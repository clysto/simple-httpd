import socket
import json
from pathlib import Path
from datetime import datetime
from os import path
from enum import Enum

DEFAULT_CONFIG = {"root": "public", "port": 8080, "index": ["index.html", "index.cgi"]}

class HttpStatus(Enum):

    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")


class Request:
    def __init__(self, request_txt):
        [head, body] = request_txt.split("\r\n\r\n")
        head = head.split("\r\n")
        request_line = head[0]
        [method, url, protocol] = request_line.split(" ")
        self.method = method
        self.url = url
        self.protocol = protocol
        self.body = body
        self.header = {}
        for i in range(1, len(head)):
            line = head[i]
            [k, v] = line.split(": ")
            self.header[k] = v

    def __str__(self):
        return str(
            {
                "method": self.method,
                "url": self.url,
                "protocol": self.protocol,
                "body": self.body,
                "header": self.header,
            }
        )


class Response:
    def __init__(self, body):
        self.body = body
        self.status = HttpStatus.OK
        self.header = {
            "Date": self.format_date(datetime.utcnow()),
            "Contene-Length": len(body),
        }

    def format_date(self, dt):
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
            weekday,
            dt.day,
            month,
            dt.year,
            dt.hour,
            dt.minute,
            dt.second,
        )

    def __str__(self):
        status = self.status.value
        response_line = f"HTTP/1.1 {status[0]} {status[1]}"
        header_lines = []
        for k, v in self.header.items():
            header_lines.append(k + ": " + str(v))
        head = response_line + "\r\n" + "\r\n".join(header_lines)
        body = self.body
        return head + "\r\n\r\n" + body

    def set_status(self, status):
        self.status = status


class HttpServer:
    def __init__(self, root, host, port):
        self.host = host
        self.port = port
        self.root = root

    def __send(self, conn, req):
        p = Path(self.root, req.url[1:])
        url = str(p.resolve())
        if not path.exists(url) or not path.isfile(url):
            # 找不到文件返回404
            res = Response("")
            res.set_status(HttpStatus.NOT_FOUND)
        else:
            # 打开指定文件返回
            with open(url, "r") as f:
                content = f.read()
                res = Response(content)
        conn.sendall(str(res).encode())

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print(addr)
                    # TODO:接收窗口调整
                    data = conn.recv(1024)
                    data = data.decode()
                    req = Request(data)
                    self.__send(conn, req)
                    conn.close()


if __name__ == "__main__":
    server = HttpServer("public", "127.0.0.1", 8080)
    server.start()
