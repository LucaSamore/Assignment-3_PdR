import sys, signal
import socketserver
import socket
from server import ServerHandler

PORT = 8080
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
server = socketserver.ThreadingTCPServer((IP_ADDRESS, PORT), ServerHandler)

def signal_handler(signal, frame):
    print("Server is shutting down...")
    try:
        if server:
            server.server_close()
    finally:
        sys.exit(0)

def main():
    print(f'Server is running at http://{IP_ADDRESS}:{PORT}')
    server.daemon_threads = True
    server.allow_reuse_address = True
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    main()