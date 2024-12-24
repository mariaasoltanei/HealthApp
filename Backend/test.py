from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory storage for demonstration purposes
# Replace with a database in production (e.g., SQLite, PostgreSQL)
sensor_data_store = []

@app.route('/sensorData/upload', methods=['POST'])
def upload_sensor_data():
    """
    Endpoint to receive sensor data from the Android app.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        # Log received data (You can save it to a database here)
        for record in data:
            record['received_at'] = datetime.datetime.now().isoformat()
            sensor_data_store.append(record)
            print(f"Received data: {record}")

        return jsonify({"message": "Data received successfully", "received_count": len(data)}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/data', methods=['GET'])
def get_all_data():
    """
    Endpoint to fetch all uploaded sensor data.
    """
    return jsonify(sensor_data_store), 200

@app.route('/activities', methods=['GET'])
def get_activities():
    activities = [
        {
            "activityName": "Running",
            "caloriesBurned": 120,
            "duration": "30 minutes",
            "averageHeartRate": 130,
            "stepsTaken": 4500,
            "activityDateTime": "2024-01-01T07:00:00Z",
            "notes": "Morning jog around the lake."
        },
        {
            "activityName": "Cycling",
            "caloriesBurned": 200,
            "duration": "45 minutes",
            "averageHeartRate": 140,
            "stepsTaken": 0,  # Not applicable for cycling
            "activityDateTime": "2024-01-02T09:00:00Z",
            "notes": "Cycling on mountain trails."
        }
    ]
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
