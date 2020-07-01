import socket
from pathlib import Path
from threading import Thread
from request import Request
from response import Response
from http_status import HttpStatus
from os import path

class HttpServer(Thread):
    def __init__(self, root, host, port, index):
        Thread.__init__(self, daemon=True)
        self.host = host
        self.port = port
        self.root = root
        self.index = index

    def __send(self, conn, req):
        p = self.__get_file(req.url[1:])
        if p is None:
            # 找不到文件返回404
            res = Response(b"")
            res.set_status(HttpStatus.NOT_FOUND)
        else:
            # 打开指定文件返回
            with p.open("rb") as f:
                content = f.read()
                res = Response(content)
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
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on http://{self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(addr)
                    # TODO:接收窗口调整
                    data = conn.recv(1024)
                    data = data.decode()
                    if not data:
                        continue
                    req = Request(data)
                    self.__send(conn, req)
                    conn.close()