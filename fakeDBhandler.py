from types import SimpleNamespace as Namespace
import json

class DBHandler:
    
    USERS_PATH = 'fake-db/users.json'
    
    def __init__(self):
        self.users = []
        self.__read_users()
    
    def add_user(self, newUser):
        self.users.append(newUser)
        self.__save_users()
    
    def does_user_exist(self, user):
        print(user.__dict__)
        return user.email in map(lambda u: u.email, self.users)
    
    def get_users(self):
        return self.users
    
    def __save_users(self):
        with open(self.USERS_PATH, 'w') as file:
            json.dump([user.__dict__ for user in self.users], file, indent=1)

    def __read_users(self):
        with open(self.USERS_PATH) as file:
            self.users = json.load(file, object_hook=lambda d: Namespace(**d))