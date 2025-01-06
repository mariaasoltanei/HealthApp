from iotdb.utils.IoTDBConstants import TSDataType
from db_session_pool import session_pool
from collections import defaultdict
import pandas as pd

def insert_sensor_data(sensor_data):
    try:
        session = session_pool.get_session()

        data_by_device = defaultdict(list)
        for record in sensor_data:
            user_id = record["userId"]
            sensor_type = record["sensorType"]
            timestamp = record["timestamp"]
            x = record["x"]
            y = record["y"]
            z = record["z"]

            device_id = f"root.users.user_{user_id}.{sensor_type}"
            data_by_device[device_id].append((timestamp, [x, y, z]))

        device_ids_ = []
        time_list_ = []
        measurements_list_ = []
        data_type_list_ = []
        values_list_ = []

        for device_id, records in data_by_device.items():
            for timestamp, values in records:
                device_ids_.append(device_id)
                time_list_.append(timestamp)
                measurements_list_.append(["x", "y", "z"])
                data_type_list_.append([TSDataType.FLOAT, TSDataType.FLOAT, TSDataType.FLOAT])
                values_list_.append(values)

        session.insert_records(
            device_ids_, time_list_, measurements_list_, data_type_list_, values_list_
        )

        print("Data inserted successfully into IoTDB.")

    except Exception as e:
        print(f"Error while inserting sensor data: {e}")

    finally:
        if session:
            session_pool.put_back(session)

def check_user_model_exists(user_id):
    try:
        session = session_pool.get_session()

        path = f"root.users.user_{user_id}.accelerometer.x"

        result = session.check_time_series_exists(path)
        if not result:
            print(f"Model for user {user_id} does not exist. Creating it...")

            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.accelerometer.x WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")
            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.accelerometer.y WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")
            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.accelerometer.z WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")

            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.gyroscope.x WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")
            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.gyroscope.y WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")
            session.execute_non_query_statement(f"CREATE TIMESERIES root.users.user_{user_id}.gyroscope.z WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY")

            print(f"Model for user {user_id} created successfully.")
        else:
            print(f"Model for user {user_id} already exists.")

    except Exception as e:
        print(f"Error while ensuring user model: {e}")

    finally:
        if session:
            session_pool.put_back(session)

def query_data(query):
    try:
        session = session_pool.get_session()
        result = session.execute_query_statement(query)

        rows = []

        while result.has_next():
            row = result.next()
            time_value = row.get_timestamp()
            field_values = [field.value for field in row.get_fields()]
            rows.append([time_value] + field_values)

        dataframe = pd.DataFrame(rows, columns=["timestamp", "x", "y", "z"])

        return dataframe

    except Exception as e:
        print(f"Error while querying sensor data: {e}")
        return None

    finally:
        if session:
            session_pool.put_back(session)

# check_user_model_exists(1)
# sensor_data = [{'sensorType': 'accelerometer', 'timestamp': 1735819501333, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501398, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501466, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501511, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501532, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501598, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501665, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501711, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501732, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501798, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501866, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501910, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501932, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}]
# #insert_sensor_data(sensor_data)
df = query_data("SELECT * FROM root.users.user_1.accelerometer")
print(df)