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
from auth import AuthorizationHandler
from http import cookies
from http.cookies import SimpleCookie

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
    _auth: AuthorizationHandler = AuthorizationHandler()
    _current_user: User = None
    
    def do_GET(self) -> None:
        
        print(self.headers)
        
        result: Optional[str] = self._router.handle_route(self.path)
        
        if result:
            self.path = result
        
        SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self) -> None:
        if self.path.find("login") != -1:
            self.__login()
        
        if self.path.find("register") != -1:
            self.__registration()
                
    def end_headers(self):
        if self._current_user and not self.headers.get('Set-Cookie'):
            cookie: SimpleCookie = self.__create_cookie()
            for morsel in cookie.values():
                self.send_header("Set-Cookie", morsel.OutputString())
            
        SimpleHTTPRequestHandler.end_headers(self)
        
    def __login(self) -> None:
        fields: dict = self.__get_login_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        loggedUser: User = self._db.find_user(fields["email"], fields["password"])
        
        if loggedUser:
            self._current_user = loggedUser
            #self.__create_authorization_header(loggedUser)
            self.path = "/pages/home.html"
            self.do_GET()
        else:
            self.send_error(401, "User not found")
        
    def __registration(self) -> None:
        fields: dict = self.__get_register_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        
        newUser: User = User(fields["name"], 
                             fields["surname"], 
                             fields["email"], 
                             self.__hash_password(fields["password"]))
        
        if self._db.try_add(newUser):
            self._current_user = newUser
            #self.__create_authorization_header(newUser)
            self.path = "/pages/home.html"
            self.do_GET()
        else:
            self.send_error(409, "Email already in used")
            
    def __hit_homepage(self) -> None:
        ...
        
    def __create_cookie(self) -> SimpleCookie:
        newCookie: SimpleCookie = cookies.SimpleCookie()
        newCookie['token'] = self._auth.encode_jwt_token(self._current_user)
        return newCookie
    
    def __create_authorization_header(self, user: User) -> None:
        self.send_header('Authorization', 'Bearer ' + self._auth.encode_jwt_token(user))
    
    def __validate_user(self, email: str, password: str) -> None:
        if not self.__validate_email(email) and self.__validate_password(password):
            self.send_error(400, "Email and/or password are not correct buddy")
    
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
            'password': form.getvalue('psw')
        }
    
    def __get_register_form_fields(self) -> dict:
        form: FieldStorage = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        
        return {
            'name': form.getvalue('name'), 
            'surname': form.getvalue('surname'), 
            'email': form.getvalue('email'), 
            'password': form.getvalue('psw')
        }