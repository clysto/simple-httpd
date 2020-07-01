from enum import Enum

class HttpStatus(Enum):

    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")
