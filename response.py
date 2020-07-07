from datetime import datetime
from http_status import HttpStatus

WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH = [
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
]


class Response:
    def __init__(self, body):
        self.body = body
        self.status = HttpStatus.OK
        self.header = {
            "Date": self.format_date(datetime.utcnow()),
            "Contene-Length": len(body),
            "Server": "simple-httpd/0.0.1",
        }

    def format_date(self, dt):
        weekday = WEEKDAY[dt.weekday()]
        month = MONTH[dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
            weekday,
            dt.day,
            month,
            dt.year,
            dt.hour,
            dt.minute,
            dt.second,
        )

    def encode(self):
        status = self.status.value
        response_line = f"HTTP/1.1 {status[0]} {status[1]}"
        header_lines = []
        for k, v in self.header.items():
            header_lines.append(k + ": " + str(v))
        head = response_line + "\r\n" + "\r\n".join(header_lines)
        body = self.body
        return head.encode() + b"\r\n\r\n" + body

    def set_status(self, status):
        self.status = status


class RawResponse:
    def __init__(self, content: bytes):
        self.status = HttpStatus.OK
        self.content = content.replace(b"\r", b"")
        self.content = content.replace(b"\n", b"\r\n")

    def set_status(self, status):
        self.status = status

    def encode(self):
        status = self.status.value
        response_line = f"HTTP/1.1 {status[0]} {status[1]}\r\n".encode()
        return response_line + self.content
