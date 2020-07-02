#!/usr/bin/env python3

import json
import os
from urllib.parse import parse_qsl

query_string = os.environ["QUERY_STRING"]
query = dict(parse_qsl(query_string))
if "name" in query:
    name = query["name"]
else:
    name = "unknowed"

print(f"<h1>Hello {name}</h1>")
