import os
import urllib.request
import unittest

BASE = os.environ.get("API1", "http://localhost:8091")


class GivenQuoteApiTests(unittest.TestCase):
    def test_each_instance_has_health_endpoint(self):
        with urllib.request.urlopen(f"{BASE}/health", timeout=10) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("instance", response.read().decode())

    def test_quote_is_available(self):
        with urllib.request.urlopen(f"{BASE}/v1/quotes", timeout=10) as response:
            self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
