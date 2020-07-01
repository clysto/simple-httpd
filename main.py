import signal
import json
import sys
from os import path
from http_server import HttpServer

DEFAULT_CONFIG = {"root": "public", "port": 8080, "index": ["index.html", "index.cgi"]}

def shutdown(sig, frame):
    sys.exit(0)

if len(sys.argv) > 1:
    config_path = sys.argv[1]
    if not path.exists(config_path) or not path.isfile(config_path):
        print("invalid config file", file=sys.stderr)
        sys.exit(-1)
    with open(config_path) as f:
        config = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            if k in config:
                DEFAULT_CONFIG[k] = config[k]

if not path.exists(DEFAULT_CONFIG["root"]) or not path.isdir(DEFAULT_CONFIG["root"]):
    print("invalid root directory", file=sys.stderr)
    sys.exit(-1)

signal.signal(signal.SIGINT, shutdown)
server = HttpServer(DEFAULT_CONFIG["root"], "127.0.0.1", DEFAULT_CONFIG["port"])
server.start()

while True:
    pass

