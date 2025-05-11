from flask import Flask, request, jsonify
import requests
import os
import time
import threading
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import numpy as np

from database_operations import insert_sensor_data

from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

with open("/app/aes-key", "rb") as f:
    base64_key = f.read().strip()

AES_KEY = base64.b64decode(base64_key)

def decrypt_value(encrypted_b64, iv_b64):
    encrypted = base64.b64decode(encrypted_b64)
    iv = base64.b64decode(iv_b64)
    aesgcm = AESGCM(AES_KEY)
    decrypted_bytes = aesgcm.decrypt(iv, encrypted, None)
    return float(decrypted_bytes.decode("utf-8"))


WORKER1_SERVICE = os.getenv("WORKER1_SERVICE", "worker1")
WORKER2_SERVICE = os.getenv("WORKER2_SERVICE", "worker2")
WORKER3_SERVICE = os.getenv("WORKER3_SERVICE", "worker3")

active_users = set()

def periodic_trigger_workers():
    while True:
        try:
            print("Triggering workers...")

            user_id = "user_1"  # make this dynamic if needed
            url1 = f"http://{WORKER1_SERVICE}:6000/trigger/user_{1}"
            url2 = f"http://{WORKER2_SERVICE}:6000/trigger/user_{1}"

            res1 = requests.post(url1, timeout=5)
            res2 = requests.post(url2, timeout=5)

            pred1 = res1.json() if res1.ok else None
            pred2 = res2.json() if res2.ok else None

            if pred1 and pred2:
                final = vote(pred1, pred2)
                print(f"Final activity for {user_id}: {final}")
            else:
                print(f"Incomplete responses for {user_id}")

        except Exception as e:
            print(f"❌ Error triggering workers: {e}")

        time.sleep(30)  # Wait 5 minutes

def vote(pred1, pred2):
    if pred1["prediction"] == pred2["prediction"]:
        return pred1["prediction"]
    return pred1["prediction"] if pred1["confidence"] > pred2["confidence"] else pred2["prediction"]


@app.route('/sensorData/aes', methods=['POST'])
def handle_aes():
    payload = request.get_json()
    data_items = payload.get("data", [])
    context = payload.get("context", {})
    user_id = context.get("user_id")

    active_users.add(user_id)

    decrypted_batch = []
    for item in data_items:
        try:
            decrypted_item = {
                "sensorType": item["sensorType"],
                "timestamp": item["timestamp"],
                "userId": item["userId"],
                "x": decrypt_value(item["x"], item["ivX"]),
                "y": decrypt_value(item["y"], item["ivY"]),
                "z": decrypt_value(item["z"], item["ivZ"])
            }
            decrypted_batch.append(decrypted_item)
        except Exception as entry_error:
            print(f"❌ Failed to decrypt AES item: {entry_error}")

    insert_sensor_data(decrypted_batch)

    return jsonify({"final_decision": "Undecided"}), 200

@app.route("/sensorData/he", methods=["POST"])
def handle_he_encrypted_prediction():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})
        user_id = context.get("user_id")
        print("Received HE encrypted data:")

        insert_sensor_data(data_items)

        return jsonify({
            "status": "success",
            "message": "Data inserted successfully"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/")
def index():
    return "🔒 Hello from Manager behind TLS!"

if __name__ == "__main__":
    trigger_thread = threading.Thread(target=periodic_trigger_workers, daemon=True)
    trigger_thread.start()

    app.run(host="0.0.0.0", port=5000)

