from types import SimpleNamespace as Namespace
from config import CONFIG
from user import User
from typing import Optional
import json
import bcrypt

class DBHandler:
        
    def __init__(self):
        self._users: list[User] = []
        self.__read_users()
    
    def try_add(self, user: User) -> bool:
        if not self.__does_user_exist(user):
            self.__add_user(user)
            return True
        return False
    
    def find_user(self, email: str, password: str) -> Optional[User]:
        return next((u for u in self._users if u.email == email and bcrypt.checkpw(password.encode('utf8'), u.password)), None)
    
    def __add_user(self, newUser: User) -> None:
        self._users.append(newUser)
        self.__save_users()
    
    def __does_user_exist(self, user: User) -> bool:
        return user.email in map(lambda u: u.email, self._users)
    
    def __save_users(self) -> None:
        with open(CONFIG['user_path'], 'w') as file:
            json.dump([user.__dict__ for user in self._users], file, indent=1)

    def __read_users(self) -> None:
        with open(CONFIG['user_path']) as file:
            self._users = json.load(file, object_hook=lambda d: Namespace(**d))