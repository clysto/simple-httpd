import socket
import mimetypes
import os
import re
from pathlib import Path
from socket import SocketIO
from threading import Thread
from request import Request
from response import Response, RawResponse
from http_status import HttpStatus
from os import path
from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor


class HttpServer(Thread):
    def __init__(self, root, port, index):
        Thread.__init__(self, daemon=True)
        self.host = "localhost"
        self.port = port
        self.root = root
        self.index = re.split(r"\s", index)
        self._running = True
        self._pool = ThreadPoolExecutor(32)

    def __send(self, conn, req: Request):
        p = self.__get_file(req.url[1:])
        if p is not None and p.suffix == ".cgi":
            # 使用cgi脚本执行
            # 创建环境变量并传递给cgi脚本
            env = os.environ.copy()
            env["QUERY_STRING"] = req.query
            env["REQUEST_METHOD"] = req.method
            cgi_script = Popen([str(p.resolve())], stdout=PIPE, env=env, stdin=PIPE)
            cgi_script.stdin.write(req.body)
            (output, err) = cgi_script.communicate()
            exit_code = cgi_script.wait()
            res = RawResponse(output)
        elif p is not None and req.method == "GET":
            # 打开指定文件返回
            with p.open("rb") as f:
                content = f.read()
                res = Response(content)
                content_type, _ = mimetypes.guess_type(str(p.resolve()))
                if content_type is not None:
                    res.header["Content-Type"] = f"{content_type}; charset=UTF-8"
        else:
            # 找不到文件返回404
            res = Response(b"")
            res.set_status(HttpStatus.NOT_FOUND)
        conn.sendall(res.encode())

    def __get_file(self, url):
        p = Path(self.root, url)
        if p.is_file():
            return p
        else:
            for try_file in self.index:
                if (p / try_file).is_file():
                    return p / try_file

        return None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket = s
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on http://{self.host}:{self.port}")
            while self._running:
                client_socket, addr = s.accept()
                self._pool.submit(self.request_handler, client_socket, addr)

    def request_handler(self, client_socket, addr):
        with client_socket:
            # TODO:接收窗口调整
            data = client_socket.recv(4096)
            if not data:
                return
            req = Request(data)
            self.__send(client_socket, req)
            client_socket.close()

    def close(self):
        self.socket.close()

