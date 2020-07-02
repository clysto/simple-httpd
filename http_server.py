import socket
import mimetypes
import os
import re
from pathlib import Path
from threading import Thread
from request import Request
from response import Response
from http_status import HttpStatus
from os import path
from subprocess import Popen, PIPE


class HttpServer(Thread):
    def __init__(self, root, port, index):
        Thread.__init__(self, daemon=True)
        self.host = "localhost"
        self.port = port
        self.root = root
        self.index = re.split(r"\s", index)

    def __send(self, conn, req: Request):
        p = self.__get_file(req.url[1:])
        if p is None:
            # 找不到文件返回404
            res = Response(b"")
            res.set_status(HttpStatus.NOT_FOUND)
        else:
            if p.suffix == ".cgi":
                # 使用cgi脚本执行
                # 创建环境变量并传递给cgi脚本
                env = os.environ.copy()
                env["QUERY_STRING"] = req.query
                print(req.query)
                cgi_script = Popen([str(p.resolve())], stdout=PIPE, env=env)
                (output, err) = cgi_script.communicate()
                print(output.decode())
                exit_code = cgi_script.wait()
                res = Response(output)
            else:
                # 打开指定文件返回
                with p.open("rb") as f:
                    content = f.read()
                    res = Response(content)
                    content_type, _ = mimetypes.guess_type(str(p.resolve()))
                    if content_type is not None:
                        res.header["Content-Type"] = f"{content_type}; charset=UTF-8"
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
            self.socket = s
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on http://{self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    # TODO:接收窗口调整
                    data = conn.recv(4096)
                    data = data.decode()
                    if not data:
                        continue
                    req = Request(data)
                    self.__send(conn, req)
                    conn.close()

    def close(self):
        self.socket.shutdown()
        