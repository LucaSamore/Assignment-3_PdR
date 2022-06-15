import re
import cgi
import bcrypt
from http.server import SimpleHTTPRequestHandler
from model import User, Session
from managers import UsersManager, SessionsManager
from router import Router
from cgi import FieldStorage
from re import Match, Pattern
from typing import Optional
from http import cookies
from http.cookies import SimpleCookie

class ServerHandler(SimpleHTTPRequestHandler):
    _router: Router = Router()
    _usersManager: UsersManager = UsersManager()
    _sessionsManager = SessionsManager()
    
    def do_GET(self) -> None:
        result: str = self._router.handle_route(self.path)
        self.send_response(200)
        if not self._sessionsManager.has_session(self.client_address[0]):
            self.path = "/pages/index.html"
        else:
            uuid_from_cookie: Optional[str] = self.__parse_cookie()
            if uuid_from_cookie:
                current_session: Session = self._sessionsManager.find_session_by_uuid(uuid_from_cookie)
                if current_session and self._sessionsManager.is_expired(current_session):
                    self._sessionsManager.delete_session(current_session)
                    self.path = "/pages/index.html"
                else:
                    self.path = result
            else:
                self.path = "/pages/index.html"
        SimpleHTTPRequestHandler.do_GET(self)
            
    def do_POST(self) -> None:
        if self.path.find("login") != -1:
            self.__login()
        
        if self.path.find("register") != -1:
            self.__registration()
            
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        SimpleHTTPRequestHandler.end_headers(self)
        
    def __login(self) -> None:
        fields: dict = self.__get_login_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        loggedUser: User = self._usersManager.find_user(fields["email"], fields["password"])
        if loggedUser:
            self.__hit_homepage(loggedUser)
        else:
            self.send_error(401, "User not found")
        
    def __registration(self) -> None:
        fields: dict = self.__get_register_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        newUser: User = User(fields["name"], 
                             fields["surname"], 
                             fields["email"], 
                             self.__hash_password(fields["password"]))
        if self._usersManager.try_add(newUser):
            self.__hit_homepage(newUser)
        else:
            self.send_error(409, "Email already in used")

    def __hit_homepage(self, user: User) -> None:
        session_uuid: str = self._sessionsManager.create_session(self.client_address[0], user)
        cookie: SimpleCookie = self.__create_cookie(session_uuid)
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/pages/home.html')
        [self.send_header("Set-Cookie", morsel.OutputString()) for morsel in cookie.values()]
        self.end_headers()

    def __create_cookie(self, uuid: str) -> SimpleCookie:
        newCookie: SimpleCookie = cookies.SimpleCookie()
        newCookie['session_id'] = uuid
        return newCookie
    
    def __parse_cookie(self) -> Optional[str]:
        if not self.headers['Cookie']:
            return None
        return self.headers['Cookie'].split("=")[1]
    
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
    
    def __get_login_form_fields(self) -> dict[str,str]:
        form: FieldStorage = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        return {
            'email': form.getvalue('email'),
            'password': form.getvalue('psw')
        }
    
    def __get_register_form_fields(self) -> dict[str,str]:
        form: FieldStorage = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        return {
            'name': form.getvalue('name'), 
            'surname': form.getvalue('surname'), 
            'email': form.getvalue('email'), 
            'password': form.getvalue('psw')
        }