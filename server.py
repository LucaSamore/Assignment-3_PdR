import re
import cgi
import bcrypt
from cgi import FieldStorage
from re import Match, Pattern
from os import path
from typing import Optional
from http.server import SimpleHTTPRequestHandler
from fakeDBhandler import DBHandler
from user import User

class Router:
    
    def handle_route(self, route: str) -> Optional[str]:
        if route == "/":
            return "/pages/index.html"
        return self.find_page(route)
    
    def find_page(self, pagePath: str) -> Optional[str]:
        if path.exists(pagePath):
            return pagePath
        return None

class ServerHandler(SimpleHTTPRequestHandler):

    _router: Router = Router()
    _db: DBHandler = DBHandler()
    
    def do_GET(self) -> None:
        
        result: Optional[str] = self._router.handle_route(self.path)
        
        if result:
            self.path = result
            self.send_response(200)
        else:
            self.send_response(404, "Page not found...")
        
        SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self) -> None:
        if self.path.find("login") != -1:
            ...
        
        if self.path.find("register") != -1:
            fields: dict = self.__get_register_form_fields()
            
            if self.__validate_user(fields['email'], fields['password']):
                newUser: User = User(fields['name'], 
                                     fields['surname'], 
                                     fields['email'], 
                                     self.__hash_password(fields['password']))
                
                if self._db.try_add(newUser):
                    self.path = "/pages/home.html"
                    self.do_GET()
                else:
                    self.send_error(409, 'Email already in used')
                
            else:
                self.send_error(400, 'Email and/or password are not correct buddy')
    
    def __validate_user(self, email: str, password: str) -> bool:
        return self.__validate_email(email) and self.__validate_password(password)
    
    def __validate_email(self, email: str) -> Optional[Match]:
        regex: Pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)

    def __validate_password(self, password: str) -> Optional[Match]:
        regex: Pattern = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        return re.fullmatch(regex, password)
    
    def __hash_password(self, toBeHashed: str) -> str:
        return str(bcrypt.hashpw(toBeHashed.encode('utf-8'), bcrypt.gensalt()), 'UTF-8')
    
    def __get_login_form_fields(self) -> dict:
        form: FieldStorage = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        
        return {
            'email': form.getvalue('email'),
            'password': form.getvalue('password')
        }
    
    def __get_register_form_fields(self) -> dict:
        form: FieldStorage = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        
        return {
            'name': form.getvalue('name'), 
            'surname': form.getvalue('surname'), 
            'email': form.getvalue('email'), 
            'password': form.getvalue('psw')
        }