from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from Database.User.Models.UserDB import UserDB

@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    birth_date: Optional[str]
    height: float
    weight: float
    gender: str
    activity_multiplier: float

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise ValueError("First name must be a string")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        #TODO: Add email validation
        self._email = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        # TODO: Add birth date validation
        self._birth_date = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be greater than zero")
        self._height = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value <= 0:
            raise ValueError("Weight must be greater than zero")
        self._weight = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value not in ['male', 'female']:
            raise ValueError("Gender must be 'male', 'female', or 'other'")
        self._gender = value

    @property
    def activity_multiplier(self):
        return self._activity_multiplier

    @activity_multiplier.setter
    def activity_multiplier(self, value):
        if not 1.0 <= value <= 2.5:
            raise ValueError("Activity multiplier must be between 1.0 and 2.5")
        self._activity_multiplier = value

    @staticmethod
    def from_userdb(userdb: UserDB) -> "User":
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

    def to_userdb(self, user_id: int) -> UserDB:
        """Convert a User instance to a UserDB instance."""
        now = datetime.now()
        return UserDB(
            id=user_id,
            created_at=now,
            updated_at=now,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            birth_date=datetime.fromisoformat(self.birth_date) if self.birth_date else None,
            height=self.height,
            weight=self.weight,
            gender=self.gender,
            activity_multiplier=self.activity_multiplier
        )