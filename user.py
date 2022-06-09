from dataclasses import dataclass

@dataclass
class User:
    name: str
    surname: str
    email: str
    password: str
    
    def full_name(self) -> str:
        return "{name} {surname}".format(name = self.name, surname = self.surname)