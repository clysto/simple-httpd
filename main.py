import signal
import json
import sys
import time
from configparser import ConfigParser
from os import path
from http_server import HttpServer


DEFAULT_CONFIG = {"root": "./", "port": 8080, "index": "index.html index.cgi"}


def shutdown(sig, frame):
    sys.exit(0)


def getconfig(config_path):
    config = {}
    user_config = ConfigParser()
    user_config.read(config_path)
    config["root"] = user_config["server"].get("root", DEFAULT_CONFIG["root"])
    config["port"] = user_config["server"].getint("port", DEFAULT_CONFIG["port"])
    config["index"] = user_config["server"].get("index", "index.html index.cgi")
    return config


def main():

    if len(sys.argv) > 1 and path.isfile(sys.argv[1]):
        # 读取用户配置
        config = getconfig(sys.argv[1])
    else:
        # 使用默认配置
        config = DEFAULT_CONFIG

    signal.signal(signal.SIGINT, shutdown)

    server = HttpServer(config["root"], config["port"], config["index"],)

    server.start()


if __name__ == "__main__":
    main()

    while True:
        time.sleep(5)
        pass

