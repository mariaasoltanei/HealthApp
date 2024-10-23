from dataclasses import dataclass
from typing import Optional

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