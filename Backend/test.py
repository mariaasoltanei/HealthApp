from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

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
            "id": 1,
            "activityName": "Running",
            "caloriesBurned": 120,
            "duration": "30 minutes",
            "averageHeartRate": 130,
            "stepsTaken": 4500,
            "activityDateTime": "2024-01-01T07:00:00Z",
            "notes": "Morning jog around the lake.",
            "activityIcon": "https://cdn2.iconfinder.com/data/icons/people-80/96/Picture13-1024.png"
        },
        {
            "id": 2,
            "activityName": "Cycling",
            "caloriesBurned": 200,
            "duration": "45 minutes",
            "averageHeartRate": 140,
            "stepsTaken": 0,  # Not applicable for cycling
            "activityDateTime": "2024-01-02T09:00:00Z",
            "notes": "Cycling on mountain trails.",
            "activityIcon": "https://cdn0.iconfinder.com/data/icons/font-awesome-solid-vol-1/640/bicycle-1024.png"
        },
        {
            "id": 3,
            "activityName": "Swimming",
            "caloriesBurned": 150,
            "duration": "1 hour",
            "averageHeartRate": 120,
            "stepsTaken": 0,  # Not applicable for swimming
            "activityDateTime": "2024-01-03T14:00:00Z",
            "notes": "Swimming in the community pool.",
            "activityIcon": "https://cdn2.iconfinder.com/data/icons/ios-7-icons/50/swimming-1024.png"
        },
        {
            "id": 4,
            "activityName": "Yoga",
            "caloriesBurned": 80,
            "duration": "1 hour",
            "averageHeartRate": 100,
            "stepsTaken": 0,  # Not applicable for yoga
            "activityDateTime": "2024-01-04T08:00:00Z",
            "notes": "Morning yoga session in the park.",
            "activityIcon": "https://cdn0.iconfinder.com/data/icons/sport-2-android-l-lollipop-icon-pack/24/yoga-1024.png"
        }
    ]
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
