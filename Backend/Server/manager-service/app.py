from flask import Flask, request, jsonify
import requests
import os

from database_operations import insert_sensor_data
from db_session_pool import get_session

app = Flask(__name__)

WORKER1_SERVICE = os.getenv("WORKER1_SERVICE", "worker1")
WORKER2_SERVICE = os.getenv("WORKER2_SERVICE", "worker2")
WORKER3_SERVICE = os.getenv("WORKER3_SERVICE", "worker3")

def store_to_iotdb(sensor_data):
    try:
        session = get_session()
        insert_sensor_data(sensor_data)
    except Exception as e:
        print(f"Error storing to IoTDB: {e}")

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
    data = request.get_json()

    # Store incoming data
    store_to_iotdb(data)

    # Send to workers
    pred1 = forward_to_worker(WORKER1_SERVICE, data)
    pred2 = forward_to_worker(WORKER2_SERVICE, data)

    final_result = vote(pred1, pred2)

    return jsonify({"final_decision": final_result})

@app.route('/sensorData/he', methods=['POST'])
def handle_he():
    data = request.get_json()

    # Store incoming data
    store_to_iotdb(data)

    # Send to Worker 3
    prediction = forward_to_worker(WORKER3_SERVICE, data)

    if prediction:
        return jsonify({"result": prediction})
    else:
        return jsonify({"error": "Worker3 unavailable"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
