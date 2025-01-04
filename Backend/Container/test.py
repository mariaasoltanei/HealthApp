from flask import Flask, request, jsonify
from validate_records import validate_records
from anomaly_detection import calculate_batch_magnitude_sum, check_gyroscope_rotation
from database_operations import check_user_model_exists, insert_sensor_data

app = Flask(__name__)

sensor_data_store = []
VALID_API_KEY = "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"

@app.route('/upload', methods=['POST'])
def upload_sensor_data():
    try:
        data = request.get_json()
        user_id = data[0]["userId"]
        trust_score = data[0]["userTrustScore"]
        sensor_type = data[0]["sensorType"]

        if not data or "userId" not in data[0] or "sensorType" not in data[0]:
            return jsonify({"error": "Invalid data format"}), 400
        
        if sensor_type not in ["accelerometer", "gyroscope"]:
            return jsonify({"error": f"Invalid sensor type"}), 400
        
        records_valid, error_message = validate_records(data)
        if not records_valid:
            trust_score = update_trust_score(user_id, 15)
            print(f"Timestamps are invalid: {error_message}")
            return jsonify({"error": error_message, "userId": user_id, "trustScore": trust_score}), 200
        
        if check_user_banned(user_id):
            return jsonify({"error": "User banned"}), 403
        
        g_force_sum = calculate_batch_magnitude_sum(data)
        g_force_threshold = 1501  
        if g_force_sum > g_force_threshold:
            trust_score = update_trust_score(user_id, 10)
            print(f"Abnormal G-force detected: {g_force_sum}")
            return jsonify({
                "error": "Abnormal G-force detected",
                "userId": user_id,
                "trustScore": trust_score
            }), 200

        max_rotation = check_gyroscope_rotation(data)
        gyroscope_threshold = 500 
        if max_rotation > gyroscope_threshold:
            trust_score = update_trust_score(user_id, 10)
            print(f"Abnormal gyroscope rotation detected: {max_rotation}")
            return jsonify({
                "error": "Abnormal gyroscope rotation detected",
                "userId": user_id,
                "trustScore": trust_score
            }), 200
        

        check_user_model_exists(user_id)
        insert_sensor_data(data)

        return jsonify({
            "message": "Data uploaded successfully" ,
            "userId": user_id,
            "trustScore": 100
        }), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/validate', methods=['POST'])
def validate_api_key():
    try:
        data = request.get_json()
        if not data or 'apiKey' not in data:
            return jsonify({"error": "API key is required"}), 400

        api_key = data['apiKey']
        if api_key == VALID_API_KEY:
            return jsonify({"valid": True}), 200
        else:
            return jsonify({"valid": False}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_all_data():
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

def update_trust_score(trust_score, deduction):
    trust_score -= deduction
    return trust_score

def check_user_banned(trust_score):
    return trust_score == 0

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

