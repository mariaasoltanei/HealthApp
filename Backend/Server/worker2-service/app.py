from flask import Flask, request, jsonify
import random
from database_operations import pull_last_5_minutes_data
import pandas as pd
import joblib
from process_data import process_data, getActivity

app = Flask(__name__)
model = joblib.load("lsvc_model.pkl")

@app.route('/trigger/<user_id>', methods=['POST'])
def trigger(user_id):
    try:
        acc_data, gyro_data = pull_last_5_minutes_data(user_id)

        acc_data = pd.DataFrame(acc_data)
        gyro_data = pd.DataFrame(gyro_data)

        df = process_data(acc_data, gyro_data)
        activity, confidence = getActivity(df, model)
        print("Activity detected:", activity)

        return jsonify({"prediction": activity, "confidence": confidence})
    except Exception as e:
        print(f"Worker error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)