from flask import Flask, request, jsonify
import random
from database_operations import pull_last_5_minutes_data
import pandas as pd

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Dummy logic: randomly decide "fall_detected" or "no_fall"
    prediction = random.choice(["walking", "standing", "sitting"])

    # Dummy logic: generate random confidence between 0.7 and 1.0
    print("this is worker 1")
    confidence = round(random.uniform(0.7, 1.0), 2)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence
    })

@app.route('/trigger', methods=['POST'])
def trigger():
    # Pull last 5 minutes data from DB and process it
    acc_data, gyro_data = pull_last_5_minutes_data('user_1')
    print(acc_data)
    print(gyro_data)
    return jsonify({"status": "Worker triggered successfully"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
