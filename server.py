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
from auth import AuthorizationHandler
from http import cookies
from http.cookies import SimpleCookie

_current_user: User = None

class ServerHandler(SimpleHTTPRequestHandler):
    _router: Router = Router()
    _usersManager: UsersManager = UsersManager()
    _sessionsManager = SessionsManager()
    _auth: AuthorizationHandler = AuthorizationHandler()
    #_current_user: User = None
    
    def do_GET(self) -> None:
        result: Optional[str] = self._router.handle_route(self.path)
        
        if result:
            self.send_response(200)
            if not self._sessionsManager.has_session(self.client_address[0]):
                self.path = "/pages/index.html"
            else:
                current_session: Session = self._sessionsManager.find_session_by_ip(self.client_address[0])
                if self._sessionsManager.is_expired(current_session):
                    self._sessionsManager.delete_session(current_session)
                    self.path = "/pages/index.html"
                else:
                    self.path = result
                # il problema è che se uno che non ha fatto il login accede alla home
                # e sul db esiste una sessione non scaduta per quell'ip, l'accesso alla home
                # avviene con successo anche senza login perché esiste una sessione con quell'ip
                # ma noi ovviamente non vogliamo questa cosa
        else:
            self.send_error(404)
        
        SimpleHTTPRequestHandler.do_GET(self)
        
        """
        result: Optional[str] = self._router.handle_route(self.path)
        
        if result:            
            self.send_response(200)
            print(self.path)
            if self._router.is_protected(self.path):
                if not self.__verify_token():
                    result = "/pages/index.html"
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', result)
            self.end_headers()
            #self.wfile.write(self.__read_page(result).encode())
        else:
            print("HEYOOO")
            self.send_error(404)
        SimpleHTTPRequestHandler.do_GET(self)
        """
            
    def do_POST(self) -> None:
        if self.path.find("login") != -1:
            self.__login()
        
        if self.path.find("register") != -1:
            self.__registration()
    
    """
    def end_headers(self):
        global _current_user
        if _current_user and not self.headers.get('Set-Cookie'):
            cookie: SimpleCookie = self.__create_cookie()
            for morsel in cookie.values():
                self.send_header("Set-Cookie", morsel.OutputString())
                #print(self.headers['Cookie'])
        SimpleHTTPRequestHandler.end_headers(self)
    """
        
    def __login(self) -> None:
        #global _current_user
        fields: dict = self.__get_login_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        loggedUser: User = self._usersManager.find_user(fields["email"], fields["password"])
        
        if loggedUser:
            #_current_user = loggedUser
            #self.__hit_homepage()
            self._sessionsManager.create_session(self.client_address[0], loggedUser)
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/pages/home.html')
            self.end_headers()
            
        else:
            self.send_error(401, "User not found")
        
    def __registration(self) -> None:
        #global _current_user
        fields: dict = self.__get_register_form_fields()
        self.__validate_user(fields["email"], fields["password"])
        
        newUser: User = User(fields["name"], 
                             fields["surname"], 
                             fields["email"], 
                             self.__hash_password(fields["password"]))
        
        if self._usersManager.try_add(newUser):
            #_current_user = newUser
            #self.__hit_homepage()
            self._sessionsManager.create_session(self.client_address[0], newUser)
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/pages/home.html')
            self.end_headers()
        else:
            self.send_error(409, "Email already in used")
            
    def __hit_homepage(self) -> None:
        ...
        
        """
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/pages/home.html')
        self.end_headers()
        """
    def __create_cookie(self) -> SimpleCookie:
        global _current_user
        newCookie: SimpleCookie = cookies.SimpleCookie()
        newCookie['token'] = self._auth.encode_jwt_token(_current_user)
        return newCookie
    
    def __verify_token(self) -> bool:
        global _current_user
        
        if not self.headers['Cookie'] or not _current_user:
            return False
        
        token: str = self.headers['Cookie'].split("=")[1][:-7]
        print("TOKEN 11111")
        print(token)
        return self._auth.is_valid(_current_user, token)
    
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
    
    def __read_page(self, pageName: str) -> str:
        with open(pageName, 'r') as page:
            return page.read()