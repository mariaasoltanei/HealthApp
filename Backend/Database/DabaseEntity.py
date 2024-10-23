from abc import ABC, abstractmethod
from datetime import datetime

class DatabaseEntity(ABC):
    @abstractmethod
    def __init__(self, id: int, created_at: datetime, updated_at: datetime):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at