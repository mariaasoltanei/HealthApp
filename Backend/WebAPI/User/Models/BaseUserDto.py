from dataclasses import dataclass
from typing import Optional

@dataclass
class BaseUserDto:
    first_name: str
    last_name: str
    email: str
    birth_date: Optional[str]
    height: float
    weight: float
    gender: str
    activity_multiplier: float
