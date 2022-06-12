from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    name: str
    surname: str
    email: str
    password: str

@dataclass
class Session:
    ip: str
    user: User
    created_at: datetime = datetime.now()
    duration: int = 1