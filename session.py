from dataclasses import dataclass
from user import User
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Session:
    ip: str
    user: User
    created_at: datetime = datetime.now()
    duration: int = 1

class SessionsManager:
    def __init__(self):
        self._sessions: list = []
    
    def create_session(self, ip: str, user: User) -> None:
        newSession: Session = Session(ip, user)
        for existing in self.find_sessions_by_user_and_ip(ip, user):
            self.delete_session(existing)
        self._sessions.append(newSession)
        
    def delete_session(self, session: Session) -> None:
        if session in self._sessions:
            self._sessions.remove(session)
    
    def has_session(self, ip: str) -> bool:
        return ip in map(lambda s: s.ip, self._sessions)
    
    def is_expired(self, session: Session) -> bool:
        return datetime.now() >= session.created_at + timedelta(hours=session.duration)
    
    def find_session_by_ip(self, ip: str) -> Optional[Session]:
        return next((s for s in self._sessions if s.ip == ip), None)
    
    def find_sessions_by_user_and_ip(self, ip: str, user: User) -> list:
        yield filter(lambda s: s.ip == ip and s.user == user, self._sessions)