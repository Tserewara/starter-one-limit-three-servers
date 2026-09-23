import json
import os
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

INSTANCE_ID = os.environ.get("INSTANCE_ID", "api-local")
WINDOW_SECONDS = 10.0
LIMIT = 10
_lock = threading.Lock()
_requests = defaultdict(deque)


def local_admission(api_key):
    now = time.monotonic()
    with _lock:
        recent = _requests[api_key]
        while recent and recent[0] <= now - WINDOW_SECONDS:
            recent.popleft()
        if len(recent) >= LIMIT:
            return False
        recent.append(now)
        return True


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def send_json(self, status, payload, headers=None):
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        for name, value in (headers or {}).items():
            self.send_header(name, str(value))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "instance": INSTANCE_ID})
            return
        if self.path != "/v1/quotes":
            self.send_json(404, {"error": "not_found"})
            return
        api_key = self.headers.get("X-Api-Key", "demo-key")
        if not local_admission(api_key):
            self.send_json(429, {"error": "rate_limited", "instance": INSTANCE_ID})
            return
        self.send_json(200, {"quote": "available", "instance": INSTANCE_ID})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
