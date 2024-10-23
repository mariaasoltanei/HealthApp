from dataclasses import dataclass
from typing import List

from WebAPI.User.Models.UserDto import UserDto

@dataclass
class UsersDto:
    users: List[UserDto] = List[UserDto]