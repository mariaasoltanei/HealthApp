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

        # print(df)
        x_features = df.values  # shape: (1, n_features)
        q_x = model.quantize_input(x_features)

        # Encrypt each sample individually
        encrypted_batch = [
            base64.b64encode(model.fhe_circuit.encrypt(q_x[i:i+1]).serialize()).decode("utf-8")
            for i in range(q_x.shape[0])
        ]

        response = requests.post(
            "http://192.168.0.102:5002/infer",
            json={"batch": encrypted_batch},
            headers={"Content-Type": "application/json"}
        )

        encrypted_predictions = []
        for enc_pred_b64 in response.json().get("predictions", []):
            encrypted_bytes = base64.b64decode(enc_pred_b64)
            enc_result = model.fhe_circuit.deserialize_result(encrypted_bytes)
            prediction = model.fhe_circuit.decrypt(enc_result)
            encrypted_predictions.append(int(prediction[0]))

        return jsonify({
            "status": "success",
            "predictions": encrypted_predictions
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5001, debug=True)

