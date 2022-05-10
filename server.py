from http.server import SimpleHTTPRequestHandler

class ServerHandler(SimpleHTTPRequestHandler):
    
    def do_POST(self):
        pass
    
    def do_GET(self):
        self.path = "/pages/index.html"
        SimpleHTTPRequestHandler.do_GET(self)
        