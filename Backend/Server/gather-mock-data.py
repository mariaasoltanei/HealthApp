from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
from database_operations import check_user_model_exists, insert_sensor_data
import pandas as pd
import numpy as np
import joblib
from concrete.ml.deployment import FHEModelClient

app = Flask(__name__)

sensor_data_log = []

@app.route("/sensorData/he", methods=["POST"])
def handle_he_encrypted_prediction():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})
        user_id = context.get("user_id")

        # Normalize and process incoming data
        for item in data_items:
            row = {
                "timestamp": item["timestamp"],
                "sensor_type": item["sensorType"],
                "user_id": item.get("userId", user_id),
                "x": item["x"],
                "y": item["y"],
                "z": item["z"]
            }
            sensor_data_log.append(row)

        df = pd.DataFrame(sensor_data_log)
        df.to_csv("sensor_data_log.csv", index=False)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001) #TODO: Change to 5000