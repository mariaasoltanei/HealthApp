import os
import time
import requests
import json
import pandas as pd
from process_data import process_data
from database_operations import pull_last_5_minutes_data
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import joblib
import tenseal as ts
import numpy as np
import base64
from flask import jsonify

WORKER1_SERVICE = os.getenv("WORKER1_SERVICE", "worker1")
WORKER2_SERVICE = os.getenv("WORKER2_SERVICE", "worker2")
WORKER3_SERVICE = os.getenv("WORKER3_SERVICE", "worker3")

def periodic_trigger_worker3(redis_client):
    while True:
        try:
            user_id= "user_1"
            now_ms = int(time.time() * 1000)
            three_minutes_ago = str(now_ms - 3 * 60 * 1000)

            stream_key = f"user:{user_id}:raw_stream"
            entries = redis_client.xrange(stream_key, min=three_minutes_ago, max="+")
            if not entries:
                print(f"No data found in the stream for user {user_id} in the last 3 minutes.")
            else:
                print("Triggering Worker3")
                raw_data = []
                for _, fields in entries:
                    try:
                        parsed = json.loads(fields["data"])
                        raw_data.append(parsed)
                    except json.JSONDecodeError:
                        continue

                df = pd.DataFrame(raw_data)
                acc_data = df[df["sensorType"] == "accelerometer"].copy()
                gyro_data = df[df["sensorType"] == "gyroscope"].copy()
                df = process_data(acc_data, gyro_data)

                scaler = joblib.load("scaler.pkl")  # Adjust path if needed
                # Normalize the processed data
                scaled_features = scaler.transform(df)

                # Create TenSEAL context
                context = ts.context(
                    ts.SCHEME_TYPE.CKKS,
                    poly_modulus_degree=8192,
                    coeff_mod_bit_sizes=[60, 40, 40, 60]
                )
                context.generate_galois_keys()
                context.global_scale = 2**40

                # Serialize context to send to worker if needed (optional)
                context_bytes = context.serialize(save_public_key=True, save_secret_key=False, save_galois_keys=True, save_relin_keys=False)

                # Encrypt feature row (assumes one row)
                encrypted_vector = ts.ckks_vector(context, scaled_features[0])
                encrypted_bytes = encrypted_vector.serialize()

                # Encode encrypted data to base64 for JSON transport
                encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
                context_b64 = base64.b64encode(context_bytes).decode('utf-8')

                payload = {
                    "encrypted_features": encrypted_b64,
                    "context": context_b64
                }

                url3 = f"http://{WORKER3_SERVICE}:6000/trigger/{user_id}"
                try:
                    res = requests.post(url3, json=payload, timeout=5)
                    if res.ok:
                        print(f"Triggered Worker3 for user: {user_id}")
                        encrypted_logits_b64 = res.json().get("encrypted_logits", [])
                        if encrypted_logits_b64:
                            # Deserialize encrypted logits
                            encrypted_logits = [ts.ckks_vector_from(context, base64.b64decode(b64)) for b64 in encrypted_logits_b64]
                            decrypted_logits = [logit.decrypt()[0] for logit in encrypted_logits]
                            predicted_label = int(np.argmax(decrypted_logits))
                            # Load encoder and convert label index to class name
                            encoder = joblib.load("encoder.pkl")
                            predicted_activity = encoder.inverse_transform([predicted_label])[0]
                            print(f"Predicted activity for {user_id}: {predicted_activity}")
                            # print(f"Predicted activity index for {user_id}: {predicted_label}")
                    else:
                        print(f"Worker3 failed to respond for user: {user_id} — Status: {res.status_code}")
                except Exception as req_error:
                    print(f"Error contacting Worker3 for user {user_id}: {req_error}")

        except Exception as e:
            print(f"Unexpected error in periodic_trigger_worker3: {e}")

        time.sleep(30)  # todo: every 3 minutes

def vote(pred1, pred2):
    if pred1["prediction"] == pred2["prediction"]:
        return pred1["prediction"]
    return pred1["prediction"] if pred1["confidence"] > pred2["confidence"] else pred2["prediction"]

def periodic_trigger_workers():
    while True:
        try:
            print("Triggering workers...")
            user_id = "user_1"
            result = pull_last_5_minutes_data(user_id)

            if not result or not isinstance(result, (list, tuple)) or len(result) != 2:
                return jsonify({"error": "Data fetch failed"}), 500

            acc_data, gyro_data = result

            if acc_data is None or gyro_data is None:
                print("No data received from DB")
            else:
                url1 = f"http://{WORKER1_SERVICE}:6000/trigger/{user_id}"
                url2 = f"http://{WORKER2_SERVICE}:6000/trigger/{user_id}"

                max_retries = 3
                delay = 2

                pred1 = pred2 = None

                for attempt in range(max_retries):
                    if not pred1:
                        res1 = requests.post(url1, timeout=5)
                        if res1.ok:
                            p1 = res1.json()
                            if "prediction" in p1 and "confidence" in p1:
                                pred1 = p1

                    if not pred2:
                        res2 = requests.post(url2, timeout=5)
                        if res2.ok:
                            p2 = res2.json()
                            if "prediction" in p2 and "confidence" in p2:
                                pred2 = p2

                    if pred1 and pred2:
                        break  # both predictions received

                    time.sleep(delay)  # wait before retrying

                if pred1 and pred2:
                    final = vote(pred1, pred2)
                    print(f"Final activity for {user_id}: {final}")
                else:
                    print(f"Could not collect both predictions after retries for {user_id}")

        except Exception as e:
            print(f"Error triggering workers: {e}")

        time.sleep(30)  # or 300 for 5 minutes