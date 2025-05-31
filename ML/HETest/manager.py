import redis, json
import threading
import base64
import numpy as np
import time
import pandas as pd
import joblib
import requests
from flask import Flask, request, jsonify
from process_data import process_data, getActivity
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from prometheus_flask_exporter import PrometheusMetrics
from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer

app = Flask(__name__)
metrics = PrometheusMetrics(app)
model = joblib.load("lsvc_concrete_model.pkl")
X_sample = np.load("sample_input.npy")
model.compile(X_sample)

redis_client = redis.Redis(host="192.168.56.11", port=6379, decode_responses=True)

@app.route("/sensorData/he", methods=["GET"])
def handle_he():
    try:
        # payload = request.get_json()
        # data_items = payload.get("data", [])
        # context = payload.get("context", {})
        user_id = "1"
        key = f"user:user_{user_id}:raw_stream"
        now_ms = int(time.time() * 1000)
        three_minutes_ago = str(now_ms - 3 * 60 * 1000)
        three_hours_ago = str(now_ms - 3 * 60 * 60 * 1000)

        # # Let's create the client and load the model
        fhemodel_client = FHEModelClient("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model", key_dir="/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model")

        # # The client first need to create the private and evaluation keys.
        # serialized_evaluation_keys = fhemodel_client.get_serialized_evaluation_keys()

        #todo: change this such that it is 3 mins ago
        entries = redis_client.xrange(key, max="+", count=1000)
        raw_data = []
        for _, fields in entries:
            try:
                parsed = json.loads(fields["data"])
                raw_data.append(parsed)
            except json.JSONDecodeError:
                continue

        df = pd.DataFrame(raw_data)

        if df.empty:
            return jsonify({"status": "error", "message": "No data in stream"}), 400

        acc_data = df[df["sensorType"] == "accelerometer"].copy()
        gyro_data = df[df["sensorType"] == "gyroscope"].copy()

        if acc_data.empty or gyro_data.empty:
            return jsonify({"error": "No data found for the last 5 minutes"}), 404

        df = process_data(acc_data, gyro_data)

        decrypted_predictions = []
        encrypted_batch = []

        for i in range(df.shape[0]):
            clear_input = df.iloc[[i]].values  # shape: (1, n_features)
            encrypted_input = fhemodel_client.quantize_encrypt_serialize(clear_input)
            encrypted_batch.append(base64.b64encode(encrypted_input).decode("utf-8"))

        response = requests.post(
            "http://192.168.0.102:5002/infer",
            json={"batch": encrypted_batch},
            headers={"Content-Type": "application/json"}
        )

        try:
            predictions_data = response.json()
            if "predictions" not in predictions_data:
                raise KeyError("Missing 'predictions' key in server response")
            for enc_pred_b64 in predictions_data["predictions"]:
                decrypted = fhemodel_client.deserialize_decrypt_dequantize(base64.b64decode(enc_pred_b64))[0]
                decrypted_predictions.append(int(decrypted))
        except KeyError as ke:
            return jsonify({"status": "error", "message": str(ke)}), 500
        except Exception as decryption_error:
            return jsonify({"status": "error", "message": f"Decryption error: {str(decryption_error)}"}), 500

        return jsonify({
            "status": "success",
            "predictions": decrypted_predictions
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5001, debug=True)

