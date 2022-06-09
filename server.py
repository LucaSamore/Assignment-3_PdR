import re
import cgi
from cgi import FieldStorage
from re import Match, Pattern
from os import path
from typing import Optional
from http.server import SimpleHTTPRequestHandler

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
    
    def do_GET(self) -> None:
        
        result: Optional[str] = self._router.handle_route(self.path)
        
        if result:
            self.path = result
            self.send_response(200)
        else:
            self.send_response(404, "Page not found...")
        print(self.path)
        #self.path = self._router.handle_route(self.path)
        #self.path = "/pages/home.html"
        SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self) -> None:
        ...        
    
    def __validate_user(self, email: str, password: str) -> bool:
        return self.__validate_email(email) and self.__validate_password(password)
    
    def __validate_email(self, email: str) -> Optional[Match]:
        regex: Pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)

    def __validate_password(self, password: str) -> Optional[Match]:
        regex: Pattern = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        return re.fullmatch(regex, password)
    
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