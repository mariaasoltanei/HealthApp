from flask import Flask, request, jsonify
import requests
import os
import time
import threading
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import numpy as np

from database_operations import insert_sensor_data
from db_session_pool import get_session

app = Flask(__name__)
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

def periodic_trigger_workers():
    while True:
        try:
            print("⏳ Triggering workers to process last 5 minutes of data...")
            requests.post(f"http://{WORKER1_SERVICE}:6000/trigger", timeout=5)
            requests.post(f"http://{WORKER2_SERVICE}:6000/trigger", timeout=5)
            print("✅ Workers triggered successfully.")
        except Exception as e:
            print(f"❌ Error triggering workers: {e}")

        time.sleep(30)  # Wait 5 minutes (300)


def forward_to_worker(worker_service, data):
    try:
        url = f"http://{worker_service}:6000/predict"
        response = requests.post(url, json=data, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Error contacting worker {worker_service}: {e}")
        return None

def vote(pred1, pred2):
    if not pred1 or not pred2:
        return "Undecided"

    if pred1["prediction"] == pred2["prediction"]:
        return pred1["prediction"]

    return pred1["prediction"] if pred1["confidence"] > pred2["confidence"] else pred2["prediction"]

@app.route('/sensorData/aes', methods=['POST'])
def handle_aes():
    payload = request.get_json()
    data_items = payload.get("data", [])
    context = payload.get("context", {})
    user_id = context.get("user_id")

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

        prediction = forward_to_worker(WORKER3_SERVICE, data_items)

        if prediction:
            return jsonify({"result": prediction})
        else:
            return jsonify({"error": "Worker3 unavailable"}), 500


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    trigger_thread = threading.Thread(target=periodic_trigger_workers, daemon=True)
    trigger_thread.start()

    app.run(host="0.0.0.0", port=5000)

