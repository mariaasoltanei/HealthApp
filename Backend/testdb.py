from iotdb.Session import Session

def create_iotdb_model(iotdb_host, iotdb_port, username, password, users):
    """
    Creates the IoTDB model for storing accelerometer and gyroscope data.

    :param iotdb_host: Hostname or IP of the IoTDB server.
    :param iotdb_port: Port of the IoTDB server.
    :param username: Username for authentication.
    :param password: Password for authentication.
    :param users: List of user IDs for whom time series should be created.
    """
    try:
        session = Session(iotdb_host, iotdb_port, username, password)
        session.open()

        for user_id in users:
            storage_group = f"root.users.user_{user_id}"

            create_accelerometer_x = f"CREATE TIMESERIES {storage_group}.accelerometer.x WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"
            create_accelerometer_y = f"CREATE TIMESERIES {storage_group}.accelerometer.y WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"
            create_accelerometer_z = f"CREATE TIMESERIES {storage_group}.accelerometer.z WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"

            create_gyroscope_x = f"CREATE TIMESERIES {storage_group}.gyroscope.x WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"
            create_gyroscope_y = f"CREATE TIMESERIES {storage_group}.gyroscope.y WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"
            create_gyroscope_z = f"CREATE TIMESERIES {storage_group}.gyroscope.z WITH DATATYPE=FLOAT, ENCODING=RLE, COMPRESSOR=SNAPPY"

            # Execute SQL statements
            session.execute_non_query_statement(create_accelerometer_x)
            session.execute_non_query_statement(create_accelerometer_y)
            session.execute_non_query_statement(create_accelerometer_z)

            session.execute_non_query_statement(create_gyroscope_x)
            session.execute_non_query_statement(create_gyroscope_y)
            session.execute_non_query_statement(create_gyroscope_z)

        print("IoTDB model created successfully.")

    except Exception as e:
        print(f"Error while creating IoTDB model: {e}")

    finally:
        if session:
            session.close()

# Configuration
iotdb_host = "192.168.0.106"  # Replace with your IoTDB host IP
iotdb_port = 6667          # Default IoTDB port
username = "root"         # IoTDB username
password = "root"         # IoTDB password


users = [1, 2, 3]  


create_iotdb_model(iotdb_host, iotdb_port, username, password, users)
