import signal
from http_server import HttpServer

DEFAULT_CONFIG = {"root": "public", "port": 8080, "index": ["index.html", "index.cgi"]}

def shutdown(sig, frame):
    exit(0)

signal.signal(signal.SIGINT, shutdown)
server = HttpServer("test/www", "127.0.0.1", 8080)
server.start()

while True:
    pass
    