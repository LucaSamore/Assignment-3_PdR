import json
from datetime import datetime
from model import User, Session
from types import SimpleNamespace as Namespace
from typing import TypeVar, Callable

T = TypeVar("T")

class DatabaseHandler:
    
    def perform_write_operation(self, strategy: Callable[[list[T], str], None]) -> None:
        strategy
    
    def perform_read_operation(self, strategy: Callable[str, list[T]]) -> list[T]:
        return strategy

class OperationStrategies:
    
    @staticmethod
    def write_users(users: list[User], path: str) -> None:
        with open(path, 'w') as file:
            json.dump([user.__dict__ for user in users], file, indent=1)
    
    @staticmethod
    def read_users(path: str) -> list[User]:
        users: list[User] = []
        with open(path) as file:
            users = json.load(file, object_hook=lambda d: Namespace(**d))
        return users
    
    @staticmethod
    def write_sessions(sessions: list[Session], path: str) -> None:
        sessions = map(lambda s: Session(s.uuid, s.ip, s.user.__dict__, s.created_at.isoformat(), s.duration), sessions)
        with open(path, 'w') as file:
            json.dump([session.__dict__ for session in sessions], file, indent=1)
    
    @staticmethod
    def read_sessions(path: str) -> list[Session]:
        sessions: list[Session] = []
        with open(path) as file:
            sessions = json.load(file, object_hook=lambda d: Namespace(**d))
        sessions = list(map(lambda s: Session(s.uuid, s.ip, s.user, datetime.strptime(s.created_at, "%Y-%m-%dT%H:%M:%S.%f"), s.duration), sessions))
        return sessions