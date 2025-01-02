import datetime

def validate_records(data):
    accel_timestamps = sorted([record.get("timestamp") for record in data if record.get("sensorType") == "accelerometer" and "timestamp" in record])
    gyro_timestamps = sorted([record.get("timestamp") for record in data if record.get("sensorType") == "gyroscope" and "timestamp" in record])

    valid_amount, amount_message = validate_amount(data)
    if not valid_amount:
        return False, amount_message
    
    if accel_timestamps:
        accel_valid, accel_message = validate_sensor_timestamps(accel_timestamps, "accelerometer")
        if not accel_valid:
            return False, accel_message
    else:
        return False, "No timestamps found for accelerometer data."

    if gyro_timestamps:
        gyro_valid, gyro_message = validate_sensor_timestamps(gyro_timestamps, "gyroscope")
        if not gyro_valid:
            return False, gyro_message
    else:
        return False, "No timestamps found for gyroscope data."

    return True, None


def validate_sensor_timestamps(timestamps, sensor_type):
    timestamps = sorted(timestamps)

    start_time = datetime.datetime.fromtimestamp(timestamps[0] / 1000.0)
    end_time = datetime.datetime.fromtimestamp(timestamps[-1] / 1000.0)
    #print(f"{sensor_type.capitalize()} - Start time: {start_time}, End time: {end_time}")

    if (end_time - start_time).total_seconds() > 11:
        return False, f"{sensor_type.capitalize()} timestamp range exceeds 10 seconds."

    for i in range(1, len(timestamps)):
        if timestamps[i] <= timestamps[i - 1]:
            return False, f"{sensor_type.capitalize()} timestamps are not sequential."

    return True, None


def validate_amount(data):
    if len(data) < 150 and len(data) > 155:
        return False, "Insufficient sensor data."

    return True, None