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