import os
import time
import urllib.error
import urllib.request

BASES = [os.environ[name] for name in ("API1", "API2", "API3")]


def quote(base, api_key):
    """(status, Retry-After header or None)."""
    req = urllib.request.Request(f"{base}/v1/quotes", headers={"X-Api-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.headers.get("Retry-After")
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Retry-After")


def new_key(prefix):
    return f"{prefix}-{time.time_ns()}"
