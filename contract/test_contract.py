"""The quotes API's given behaviour, black-box. A port passes these."""

import json
import os
import time
import unittest
import urllib.error
import urllib.request

BASES = [os.environ.get(n, f"http://localhost:{p}") for n, p in (("API1", 8091), ("API2", 8092), ("API3", 8093))]


def get(url, key=None):
    req = urllib.request.Request(url, headers={"X-Api-Key": key} if key else {})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


class Contract(unittest.TestCase):
    def test_every_instance_reports_its_name(self):
        names = {get(f"{b}/health")[1]["instance"] for b in BASES}
        self.assertEqual(len(names), 3)

    def test_a_quote(self):
        status, body = get(f"{BASES[0]}/v1/quotes", f"contract-{time.time_ns()}")
        self.assertEqual(status, 200)
        self.assertEqual(body["quote"], "available")

    def test_eleventh_request_on_one_instance_is_429(self):
        key = f"contract-{time.time_ns()}"
        statuses = [get(f"{BASES[0]}/v1/quotes", key)[0] for _ in range(11)]
        self.assertEqual(statuses[:10], [200] * 10)
        self.assertEqual(statuses[10], 429)
        self.assertEqual(get(f"{BASES[0]}/v1/quotes", key)[1]["error"], "rate_limited")

    def test_unknown_route_is_404(self):
        self.assertEqual(get(f"{BASES[0]}/nope")[0], 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
