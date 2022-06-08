import sys, signal
import socketserver
from config import CONFIG
from server import ServerHandler

server = socketserver.ThreadingTCPServer((CONFIG['address'], CONFIG['port']), ServerHandler)

def signal_handler(signal, frame):
    print("Server is shutting down...")
    try:
        if server:
            server.server_close()
    finally:
        sys.exit(0)

def main():
    print(f'Server is running at http://{CONFIG["address"]}:{CONFIG["port"]}')
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