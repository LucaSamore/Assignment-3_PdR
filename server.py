from http.server import SimpleHTTPRequestHandler
from http import cookies
from fakeDBhandler import DBHandler
import cgi
import re
import jwt
import bcrypt

SECRET='tellnobody'

class User: pass

class ServerHandler(SimpleHTTPRequestHandler):
    DB = DBHandler()
    
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        email = form.getvalue('email')
        password = form.getvalue('psw')
        
        if self.path.find("signIn") != -1:
            # validate email and password
            # check if the user exists
            # create a token if the user hasn't one yet
            # hit the homepage
            pass
        
        if self.path.find("signUp") != -1:
            if self.__validate_email(email) and self.__validate_password(password):
                newUser = User()
                newUser.email = email
                newUser.password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), 'UTF-8')
                
                if not self.DB.does_user_exist(newUser):
                    
                    # create a new token for the user
                    token = self.__create_token(newUser)
                    
                    # save the new user
                    self.DB.add_user(newUser)
                    
                    # create a cookie and send it to the user
                    cookie = cookies.SimpleCookie()
                    cookie['access_token'] = token                
                    
                    # hit the homepage
                else:
                    self.send_error(409, 'Email already in used')
            else:
                self.send_error(400, "Don't mess with me...")
        
    def do_GET(self):
        if not self.__is_authorized():
            #self.send_error(401, "You're not authenticated bud")
            self.__response("index.html")
            return
        
        if self.path == "/":
            self.__response("home.html")
            return
        
    def __is_authorized(self):
        return self.headers.get('Authorization') is not None
    
    def __response(self, fileName):
        self.send_response(200)
        self.path = f"/pages/{fileName}"
        SimpleHTTPRequestHandler.do_GET(self)
        
    def __create_token(self, user):
        return jwt.encode(user.__dict__, SECRET, algorithm="HS256")
    
    def __decode_token(self, token):
        return jwt.decode(token, SECRET, algorithms=["HS256"])
        
    def __validate_email(self, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)
    
    def __validate_password(self, password):
        regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        return re.fullmatch(regex, password)