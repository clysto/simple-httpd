#!/usr/bin/env python3

import os
import sys
import json
from urllib.parse import parse_qsl

query_string = os.environ["QUERY_STRING"]
query = dict(parse_qsl(query_string))
if "name" in query:
    name = query["name"]
else:
    name = "unknowed"

print("Server: simple-httpd/0.0.1")
print("Content-Type: application/json")
print("\n\n", end="")

body = sys.stdin.read(2048)

print(body)

