
import pandas as pd
import joblib
import redis
import json
import time
from flask import Flask, request, jsonify
from process_data import process_data, getActivity
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
#model = joblib.load("rf_model.pkl")

@app.route('/trigger/<user_id>', methods=['POST'])
def trigger(user_id):
    try:
        r = redis.Redis(host="redis", port=6379, decode_responses=True)
        stream_key = f"user:{user_id}:raw_stream"

        now_ms = int(time.time() * 1000)
        three_minutes_ago = str(now_ms - 3 * 60 * 1000)

        entries = r.xrange(stream_key, min=three_minutes_ago, max="+")

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
        #activity, confidence = getActivity(df, model)

        print(df)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
