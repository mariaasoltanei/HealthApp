from iotdb.utils.IoTDBConstants import TSDataType
from db_session_pool import get_session_pool
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta

session_pool = get_session_pool()

def insert_sensor_data(sensor_data):
    session = None
    try:
        session = session_pool.get_session()
        session.open()

        data_by_device = defaultdict(list)
        for record in sensor_data:
            user_id = record["userId"]
            sensor_type = record["sensorType"]
            timestamp = record["timestamp"]
            x = record["x"]
            y = record["y"]
            z = record["z"]
#todo change here for HE
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
            session.close()

def check_user_model_exists(user_id):
    session = None
    try:
        session = session_pool.get_session()
        session.open()

        path = f"root.he.users.user_{user_id}.accelerometer.x"

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
            session.close()

def query_data(query):
    session = None
    try:
        session = session_pool.get_session()
        session.open()
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
            session.close()

def list_timeseries():
    session = None
    try:
        session = session_pool.get_session()
        session.open()

        result = session.execute_query_statement("SHOW TIMESERIES")

        rows = []
        column_names = result.get_column_names()  # Dynamically get correct columns

        while result.has_next():
            row = result.next()
            fields = [field.value for field in row.get_fields()]
            rows.append(fields)

        df = pd.DataFrame(rows, columns=column_names)
        return df

    except Exception as e:
        print(f"Error while listing time series: {e}")
        return None

    finally:
        if session:
            session_pool.put_back(session)
            session.close()

# df = list_timeseries()
# print(df)
# check_user_model_exists(1)
# df = query_data("SELECT * FROM root.users.user_1.accelerometer")
# print(df)
# # sensor_data = [{'sensorType': 'accelerometer', 'timestamp': 1735819501333, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501398, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501466, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501511, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501532, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501598, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501665, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501711, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501732, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501798, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501866, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}, {'sensorType': 'gyroscope', 'timestamp': 1735819501910, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 0.0, 'z': 0.0}, {'sensorType': 'accelerometer', 'timestamp': 1735819501932, 'userId': 1, 'userTrustScore': 100, 'x': 0.0, 'y': 9.809989, 'z': 0.0}]
# # insert_sensor_data(sensor_data)
# df = query_data("SELECT * FROM root.users.user_1.accelerometer")
# print(df)
# df = query_data("SHOW TIMESERIES")
# print(df)
# df["datetime"] = pd.to_datetime(df["timestamp"], unit='ms')
# df["datetime_str"] = df["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
# print(df)
# print("------------------------------------------------")
# acc_df, gyro_df = pull_last_5_minutes_data('user_1')
# print("Accelerometer Data:")
# print(acc_df)
# print("Gyroscope Data:")

# gyro_df.rename(columns={'Time': 'timestamp'}, inplace=True)
# print(gyro_df)
# session_pool.get_session().close()