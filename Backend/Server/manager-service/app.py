import redis, json
import threading
import numpy as np
import os
from flask import Flask, request, jsonify
from decrypt_aes import decrypt_value
from triggers import periodic_trigger_worker3, periodic_trigger_workers
from database_operations import insert_sensor_data
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

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
            print(f"Failed to decrypt AES item: {entry_error}")

    insert_sensor_data(decrypted_batch)

    return jsonify({"final_decision": "Undecided"}), 200

@app.route("/sensorData/he", methods=["POST"])
def handle_he():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})
        user_id = str(context.get("user_id"))
        key = f"user:user_{user_id}:raw_stream"

        for item in data_items:
            redis_client.xadd(
                key,
                {"data": json.dumps(item)},
            )

        return jsonify({
            "status": "success",
            "message": "Data inserted successfully"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/")
def index():
    return "TLS OK"

if __name__ == "__main__":
    trigger_thread = threading.Thread(target=periodic_trigger_workers, daemon=True)
    trigger_thread.start()

    trigger_worker3_thread = threading.Thread(target=periodic_trigger_worker3, args=(redis_client,), daemon=True)
    trigger_worker3_thread.start()

    app.run(host="0.0.0.0", port=5000)

