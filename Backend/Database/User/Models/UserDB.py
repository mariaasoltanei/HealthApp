from datetime import datetime

from Database.DabaseEntity import DatabaseEntity


class UserDB(DatabaseEntity):
    def __init__(self, id: int, created_at: datetime, updated_at: datetime, 
                 first_name: str, last_name: str, email: str, birth_date: datetime,
                 height: float, weight: float, gender: str, activity_multiplier: float):
        super().__init__(id, created_at, updated_at)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity_multiplier = activity_multiplier

    def to_dict(self):
        """Convert the UserDB object to a dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "height": self.height,
            "weight": self.weight,
            "gender": self.gender,
            "activity_multiplier": self.activity_multiplier
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a UserDB object from a dictionary."""
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            birth_date=datetime.fromisoformat(data["birth_date"]) if data["birth_date"] else None,
            height=data["height"],
            weight=data["weight"],
            gender=data["gender"],
            activity_multiplier=data["activity_multiplier"]
        )

    # @staticmethod
    # def from_user(user: User, user_id: int) -> "UserDB":
    #     """Convert a User instance to a UserDB instance."""
    #     now = datetime.now()
    #     return UserDB(
    #         id=user_id,
    #         created_at=now,
    #         updated_at=now,
    #         first_name=user.first_name,
    #         last_name=user.last_name,
    #         email=user.email,
    #         birth_date=datetime.fromisoformat(user.birth_date) if user.birth_date else None,
    #         height=user.height,
    #         weight=user.weight,
    #         gender=user.gender,
    #         activity_multiplier=user.activity_multiplier
    #     )

    # def to_user(self) -> User:
    #     """Convert a UserDB instance to a User instance."""
    #     return User(
    #         first_name=self.first_name,
    #         last_name=self.last_name,
    #         email=self.email,
    #         birth_date=self.birth_date.isoformat() if self.birth_date else None,
    #         height=self.height,
    #         weight=self.weight,
    #         gender=self.gender,
    #         activity_multiplier=self.activity_multiplier
    #     )