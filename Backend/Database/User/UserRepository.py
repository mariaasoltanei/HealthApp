from Database.User.Models.UserDB import UserDB
from Database.IoTDBConnection import IoTDBConnection
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
class UserRepository:

    def __init__(self):
        self.db_connection = IoTDBConnection()

    def create_timeseries(self):
        """Create the IoTDB database and time-series schema for user data."""
        try:
            # Check if the database exists
            query_database = "SHOW DATABASES"
            databases = []
            result = self.db_connection.execute_query(query_database)

            while result.has_next():
                fields = result.next().get_fields()
                databases.append(fields[0].get_string_value())  # Correctly access string value
            result.close_operation_handle()

            if "root.users" not in databases:
                self.db_connection.execute_non_query("CREATE DATABASE root.users")
                print("Database 'root.users' created.")

            # Check if the timeseries exists
            query_timeseries = "SHOW TIMESERIES root.users.profile"
            result = self.db_connection.execute_query(query_timeseries)

            if not result.has_next():  # Timeseries doesn't exist
                self.db_connection.execute_non_query(
                    "CREATE TIMESERIES root.users.profile WITH DATATYPE=TEXT, ENCODING=PLAIN"
                )
                print("Timeseries 'root.users.profile' created.")
            result.close_operation_handle()

        except Exception as e:
            print(f"Error initializing IoTDB schema: {e}")

    def add_user_to_iotdb(self, user_db: UserDB):
        """Add a user record to IoTDB."""
        try:
            device = f"root.users.{user_db.id}"  # Device path
            timestamp = int(datetime.now().timestamp() * 1000)  # Timestamp in milliseconds

            # Prepare the profile data as a JSON-like string
            profile_data = user_db.to_dict()  # Convert the UserDB object to a dictionary
            profile_string = str(profile_data).replace("'", '"')  # Convert to JSON-like format
            self.db_connection.insert_record()
            # Insert the record
            self.db_connection.insert_record(
                device=device,
                timestamp=timestamp,
                measurements=["profile"],  # Measurement name
                values=[profile_string]  # Corresponding value as a list
            )
            print(f"User {user_db.first_name} inserted into IoTDB.")
        except Exception as e:
            print(f"Error adding user to IoTDB: {e}")

    def find_user_by_id(self, user_id: int) -> UserDB:
        """Retrieve a user record from IoTDB by user ID."""
        try:
            query = f"SELECT profile FROM root.users.{user_id}"
            result = self.db_connection.execute_query(query)
            if result:
                while result.has_next():
                    row = result.next()
                    user_data = eval(row.get_fields()[0])  # Convert string back to dictionary
                    result.close_operation_handle()
                    return UserDB.from_dict(user_data)
        except Exception as e:
            print(f"Error retrieving user from IoTDB: {e}")
        return None

# class UserRepository:

#     def __init__(self):
#         self.db_connection = IoTDBConnection()

#     def create_timeseries(self):
#         """Create the IoTDB time-series schema for user data."""
#         self.db_connection.execute_non_query("CREATE STORAGE GROUP IF NOT EXISTS root.users")
#         self.db_connection.execute_non_query("""
#             CREATE TIMESERIES IF NOT EXISTS root.users.profile WITH DATATYPE=TEXT, ENCODING=PLAIN
#         """)

#     def add_user_to_iotdb(self, user_db: UserDB):
#         device = f"root.users.{user_db.id}"
#         timestamp = int(datetime.now().timestamp() * 1000)
#         profile_data = user_db.to_dict()
#         profile_string = str(profile_data).replace("'", '"')
#         self.db_connection.insert_record(device, timestamp, ["profile"], [profile_string])


#     def find_user_by_id(self, user_id: int) -> UserDB:
#         query = f"SELECT profile FROM root.users.{user_id}"
#         result = self.db_connection.execute_query(query)
#         if result:
#             while result.has_next():
#                 row = result.next()
#                 user_data = eval(row.get_fields()[0].get_string())
#                 result.close_operation_handle()
#                 return UserDB.from_dict(user_data)
#         return None


# class UserRepository:
#     def __init__(self, db_connection: IoTDBConnection):
#         self.db_connection = db_connection

#     def get_user_data(self, user_id: str):
#         query = f"SELECT * FROM root.users WHERE user_id = '{user_id}'"
#         result = self.db_connection.execute_query(query)
#         return result

#     def create_user(self, user: UserDB):
#             device = f"root.users.{user.id}"  
#             timestamp = int(user.created_at.timestamp() * 1000)  # IoTDB expects timestamp in milliseconds

#             measurements = ["first_name", "last_name", "email", "birth_date", "height", "weight", "gender", "activity_multiplier"]
#             values = [
#                 user.first_name,
#                 user.last_name,
#                 user.email,
#                 user.birth_date.strftime('%Y-%m-%d'),
#                 user.height,
#                 user.weight,
#                 user.gender,
#                 user.activity_multiplier
#             ]

#             self.db_connection.session.insert_record(device, timestamp, measurements, values)
#             print(f"User {user.first_name} inserted into IoTDB.")

