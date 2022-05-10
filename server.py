from http.server import SimpleHTTPRequestHandler
import cgi
import json
import re
import jwt
import bcrypt

SECRET='tellnobody'
users = []

class User:
    pass

class ServerHandler(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server, directory):
        users = self._read_users()
    
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
                newUser.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # create a new token for the user
                # save the new user
                # create a cookie and send it to the user
                # hit the homepage
            else:
                self.send_error(400, "Don't mess with me...")
        
        
    def do_GET(self):
        if not self._is_authorized():
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
        
    def __get_token(self, user):
        return jwt.encode(user, SECRET, algorithm="HS256")
    
    def __decode_token(self, token):
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    
    def __does_user_exist(self, user):
        return user in users
        
    def __validate_email(self, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)
    
    def __validate_password(self, password):
        regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        return re.fullmatch(regex, password)
    
    def __save_users(self):
        with open('users.json', 'w') as file:
            json.dump(users, file)
    
    def __read_users(self):
        with open('users.json') as file:
            users = json.load(file)