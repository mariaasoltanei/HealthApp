from Database.User.Models.UserDB import UserDB
from Database.IoTDBConnection import IoTDBConnection

class UserRepository:
    def __init__(self, db_connection: IoTDBConnection):
        self.db_connection = db_connection

    def get_user_data(self, user_id: str):
        query = f"SELECT * FROM root.users WHERE user_id = '{user_id}'"
        result = self.db_connection.execute_query(query)
        return result

    def create_user(self, user: UserDB):
            device = f"root.users.{user.id}"  
            timestamp = int(user.created_at.timestamp() * 1000)  # IoTDB expects timestamp in milliseconds

            measurements = ["first_name", "last_name", "email", "birth_date", "height", "weight", "gender", "activity_multiplier"]
            values = [
                user.first_name,
                user.last_name,
                user.email,
                user.birth_date.strftime('%Y-%m-%d'),
                user.height,
                user.weight,
                user.gender,
                user.activity_multiplier
            ]

            self.db_connection.session.insert_record(device, timestamp, measurements, values)
            print(f"User {user.first_name} inserted into IoTDB.")

