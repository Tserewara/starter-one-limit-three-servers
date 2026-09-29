"""60 requests for one new key, all at once: 20 to each instance, released
together from 60 threads with their connections already open."""

import http.client
import socket
import threading
from urllib.parse import urlsplit

from common import BASES, new_key

key = new_key("merchant-burst")
targets = [urlsplit(b) for b in BASES for _ in range(20)]
start = threading.Barrier(len(targets))
statuses = [None] * len(targets)


def one(i, target):
    conn = http.client.HTTPConnection(socket.gethostbyname(target.hostname), target.port, timeout=10)
    conn.connect()
    start.wait(timeout=10)
    conn.request("GET", "/v1/quotes", headers={"X-Api-Key": key, "Host": target.netloc})
    statuses[i] = conn.getresponse().status
    conn.close()


threads = [threading.Thread(target=one, args=(i, t)) for i, t in enumerate(targets)]
for t in threads:
    t.start()
for t in threads:
    t.join()
admitted = statuses.count(200)
print(f"requests={len(statuses)} concurrent admitted={admitted} rejected={statuses.count(429)} limit=10", flush=True)
