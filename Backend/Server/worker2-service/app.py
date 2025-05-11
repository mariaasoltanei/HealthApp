from flask import Flask, request, jsonify
import random
from database_operations import pull_last_5_minutes_data
import pandas as pd
import joblib
from process_data import process_data, getActivity

from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
model = joblib.load("lsvc_model.pkl")

@app.route('/trigger/<user_id>', methods=['POST'])
def trigger(user_id):
    try:
        result = pull_last_5_minutes_data(user_id)

        if not result or not isinstance(result, (list, tuple)) or len(result) != 2:
            return jsonify({"error": "Data fetch failed"}), 500

        acc_data, gyro_data = result

        if acc_data is None or gyro_data is None:
            return jsonify({"error": "No data received from DB"}), 500

        acc_data = pd.DataFrame(acc_data)
        gyro_data = pd.DataFrame(gyro_data)

        if acc_data.empty or gyro_data.empty:
            return jsonify({"error": "No data found for the last 5 minutes"}), 404

        df = process_data(acc_data, gyro_data)
        activity, confidence = getActivity(df, model)
        print("Activity detected:", activity)

        return jsonify({"prediction": activity, "confidence": confidence})
    except Exception as e:
        print(f"Worker error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)