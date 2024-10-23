from dataclasses import dataclass
from typing import Optional

from WebAPI.User.Models.BaseUserDto import BaseUserDto

@dataclass
class UserDto(BaseUserDto):
    user_id: int
