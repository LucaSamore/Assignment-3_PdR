from dataclasses import dataclass
from user import User
from datetime import datetime, timedelta

@dataclass
class Session:
    ip: str
    user: User
    created_at: datetime = datetime.now()
    duration: int = 1

class SessionsManager:
    
    def __init__(self):
        self._sessions: set = {}
    
    def create_session(self, ip: str, user: User) -> None:
        newSession = Session(ip, user)
        self._sessions.add(newSession)
        
    def delete_session(self, session: Session) -> None:
        if session in self._sessions:
            self._sessions.remove(session)
            
    def delete_if_expired(self, session: Session) -> None:
        if self.is_expired(session):
            self.delete_session(session)
    
    def is_expired(self, session: Session) -> bool:
        return session.created_at >= session.created_at + timedelta(hours=session.duration)