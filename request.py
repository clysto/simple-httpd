from urllib.parse import urlparse
class Request:

    def __init__(self, request_txt):
        tmp = request_txt.split("\r\n\r\n")
        head = tmp[0]
        body = tmp[1] if len(tmp) > 1 else ""
        head = head.split("\r\n")
        request_line = head[0]
        [method, url, protocol] = request_line.split(" ")
        self.method = method
        parsed_url = urlparse(url)
        self.url = parsed_url.path
        self.query = parsed_url.query
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