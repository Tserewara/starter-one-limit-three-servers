"""A well-behaved client: it fills one new key's quota across the three
instances, reads the 429's Retry-After, waits exactly that long, and tries
again."""

import time

from common import BASES, new_key, quote

key = new_key("merchant-retry")
status, retry_after = 200, None
sent = 0
while status == 200 and sent < 40:
    status, retry_after = quote(BASES[sent % 3], key)
    sent += 1
print(f"after {sent} requests: status={status} retry_after={retry_after if retry_after is not None else 'none'}", flush=True)
if status != 429 or retry_after is None or not retry_after.strip().isdigit():
    print("no usable Retry-After: waiting the full 10-second window instead", flush=True)
    wait = 10
else:
    wait = int(retry_after)
time.sleep(wait)
status, _ = quote(BASES[sent % 3], key)
print(f"after waiting {wait}s: status={status}", flush=True)
