from Database.User.UserRepository import UserRepository
from Domain.User.Models.User import User
from Domain.User.Models.UserMappingExtensions import user_to_userdb, userdb_to_user

class UserService:
    """Service layer for user-related operations."""
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, user: User):
        user_id = "1"
        user_db = user_to_userdb(user, user_id)
        print("Service message:",user_db)

        self.user_repository.add_user_to_iotdb(user_db)

        return {"message": "User registered successfully"}

    def get_user_by_id(self, user_id: int) -> User:
        # Retrieve from IoTDB and convert to User
        user_db = self.user_repository.find_user_by_id(user_id)
        if not user_db:
            raise ValueError("User not found")
        return userdb_to_user(user_db)