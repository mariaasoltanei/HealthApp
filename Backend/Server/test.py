from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
from database_operations import check_user_model_exists, insert_sensor_data

import numpy as np
import joblib
from concrete.ml.deployment import FHEModelClient

app = Flask(__name__)
# fhe_model = FHEModelClient.load() 

with open("Backend/Server/aes_key.txt", "r") as f:
    base64_key = f.read().strip()

AES_KEY = base64.b64decode(base64_key)

def decrypt_value(encrypted_b64, iv_b64):
    encrypted = base64.b64decode(encrypted_b64)
    iv = base64.b64decode(iv_b64)
    aesgcm = AESGCM(AES_KEY)
    decrypted_bytes = aesgcm.decrypt(iv, encrypted, None)
    return float(decrypted_bytes.decode("utf-8"))


@app.route("/sensorData/aes", methods=["POST"])
def handle_aes():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})
        user_id = context.get("user_id")
        print(data_items)

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

        # insert_sensor_data(decrypted_batch)

        return jsonify({
            "status": "success",
            "encryption": "aes",
            "count": len(decrypted_batch),
            "first_item": decrypted_batch[0] if decrypted_batch else None
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/sensorData/he", methods=["POST"])
def handle_he_encrypted_prediction():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})
        user_id = context.get("user_id")
        print(data_items)

        return jsonify({
            "status": "success",

        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/heartRate", methods=["POST"])
def handle_heart_rate():
    try:
        payload = request.get_json()
        context = payload.get("context", {})
        data = payload.get("data", [])

        requires_he = context.get("requires_he", False)
        user_id = context.get("user_id")
        print(data)

        print(f"Context: requires_he = {requires_he}")

        # Optionally log/store in IoTDB or DB here

        return jsonify({
            "status": "success",
            "requires_he": requires_he,
            "first_entry": data[0] if data else {}
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to process heart rate",
            "details": str(e)
        }), 400


@app.route("/test", methods=["GET"])
def test():
    print("Test endpoint hit.")
    return {"status": "success"}, 200
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001) #TODO: Change to 5000