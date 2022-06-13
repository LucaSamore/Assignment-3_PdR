import uuid
import bcrypt
from model import User, Session
from config import CONFIG
from typing import Optional
from database import DatabaseHandler, OperationStrategies
from datetime import datetime, timedelta

class UsersManager:
    def __init__(self):
        self._db = DatabaseHandler()
        self._users: list[User] = []
        self.__read_users()
    
    def try_add(self, user: User) -> bool:
        if not self.__does_user_exist(user):
            self.__add_user(user)
            return True
        return False
    
    def find_user(self, email: str, password: str) -> Optional[User]:
        return next((u for u in self._users if u.email == email and bcrypt.checkpw(password.encode('utf-8'), u.password.encode('utf-8'))), None)
    
    def __add_user(self, newUser: User) -> None:
        self._users.append(newUser)
        self.__save_users()
    
    def __does_user_exist(self, user: User) -> bool:
        return user.email in map(lambda u: u.email, self._users)
    
    def __save_users(self) -> None:
        self._db.perform_write_operation(OperationStrategies.write_users(self._users, CONFIG['user_path']))

    def __read_users(self) -> None:
        self._users = self._db.perform_read_operation(OperationStrategies.read_users(CONFIG['user_path']))

class SessionsManager:
    def __init__(self):
        self._db = DatabaseHandler()
        self._sessions: list[Session] = []
        self.__read_sessions()
    
    def create_session(self, ip: str, user: User) -> str:
        newSession: Session = Session(str(uuid.uuid4()), ip, user, datetime.now(), 1)
        filtered: list[Session] = self.__find_sessions_by_user_and_ip(ip, user)
        for existing in filtered:
            self.delete_session(existing)
        self._sessions.append(newSession)
        self.__save_sessions()
        return newSession.uuid
        
    def delete_session(self, session: Session) -> None:
        if session in self._sessions:
            self._sessions.remove(session)
    
    def has_session(self, ip: str) -> bool:
        return ip in map(lambda s: s.ip, self._sessions)
    
    def is_expired(self, session: Session) -> bool:
        return datetime.now() >= session.created_at + timedelta(hours=session.duration)
    
    def find_session_by_uuid(self, givenUUID: str) -> Optional[Session]:
        return next((s for s in self._sessions if s.uuid == givenUUID), None)

    def __find_sessions_by_user_and_ip(self, ip: str, user: User) -> list[Session]:
        return list(filter(lambda s: s.ip == ip and s.user == user, self._sessions))
    
    def __save_sessions(self) -> None:
        self._db.perform_write_operation(OperationStrategies.write_sessions(self._sessions, CONFIG['session_path']))
    
    def __read_sessions(self) -> None:
        self._sessions = self._db.perform_read_operation(OperationStrategies.read_sessions(CONFIG['session_path']))