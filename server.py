from http.server import SimpleHTTPRequestHandler
from fakeDBhandler import DBHandler
from htmlIndex import index_page
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
                    
                    # set Authorization header with Bearer {token}
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Authorization', 'Bearer ' + token)
                    self.send_header('Location','/home.html')
                    self.end_headers()
                    
                    # hit the homepage
                    self.wfile.write(bytes(self.__read_page("home.html"), 'utf-8'))
                    
                else:
                    self.send_error(409, 'Email already in used')
            else:
                self.send_error(400, "Don't mess with me...")
        
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if not self.__is_authorized():
            #self.send_error(401, "You're not authenticated bud")
            self.wfile.write(bytes(index_page(self, 8080, self.client_address[0]), 'utf-8'))
            return
        
        print(self.path)
        self.wfile.write(bytes(self.__read_page(self.path), 'utf-8'))
        
    def __is_authorized(self):
        return self.headers.get('Authorization') is not None
        
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
    
    def __read_page(self, pageName):
        with open(f'pages/{pageName}', 'r') as page:
            return page.read()