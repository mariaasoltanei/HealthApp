
from Domain.User.Models.User import User
from Database.User.Models.UserDB import UserDB
from datetime import datetime

def user_to_userdb(user: User, user_id: int) -> UserDB:
    """Convert a User instance to a UserDB instance."""
    now = datetime.now()
    return UserDB(
        id=user_id,
        created_at=now,
        updated_at=now,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        birth_date=datetime.fromisoformat(user.birth_date) if user.birth_date else None,
        height=user.height,
        weight=user.weight,
        gender=user.gender,
        activity_multiplier=user.activity_multiplier
    )

def userdb_to_user(userdb: UserDB) -> User:
    """Convert a UserDB instance to a User instance."""
    return User(
        first_name=userdb.first_name,
        last_name=userdb.last_name,
        email=userdb.email,
        birth_date=userdb.birth_date.isoformat() if userdb.birth_date else None,
        height=userdb.height,
        weight=userdb.weight,
        gender=userdb.gender,
        activity_multiplier=userdb.activity_multiplier
    )
