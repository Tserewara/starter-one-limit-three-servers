"""The carrier sale, small: 30 requests for one new key, one at a time,
round-robin across the three instances, well inside one 10-second window."""

from common import BASES, new_key, quote

key = new_key("merchant-017")
statuses = [quote(BASES[i % 3], key)[0] for i in range(30)]
admitted = statuses.count(200)
print(f"requests=30 admitted={admitted} rejected={30 - admitted} limit=10 window_seconds=10")
