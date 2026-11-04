#!/usr/bin/env python3

import requests
import sys

try:
    BASE = sys.argv[1]
except IndexError:
    print(
        f"please pass the base URL, e.g. {sys.argv[0]} http://localhost:9080/"
    )
    sys.exit(1)

hits = {200: 0, 502: 0}
first_502 = None
last_502 = None
for n in range(3300, 3900):
    url = BASE + "a" * (n - 2) + "/"
    resp = requests.head(url)
    hits[resp.status_code] += 1
    if resp.status_code != 200:
        first_502 = len(url) if first_502 is None else first_502
        last_502 = len(url)
    print(f"length {len(url)}: {resp.status_code}")
print(f"first 502 at len(url) = {first_502}, last 502 at {last_502}")
print(hits)
