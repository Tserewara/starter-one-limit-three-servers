import os
import time
import urllib.request

BASES = [os.environ[name] for name in ("API1", "API2", "API3")]
api_key = f"merchant-017-{time.time_ns()}"
results = []
for index in range(30):
    request = urllib.request.Request(f"{BASES[index % 3]}/v1/quotes", headers={"X-Api-Key": api_key})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            results.append(response.status)
    except urllib.error.HTTPError as error:
        results.append(error.code)
admitted = sum(status == 200 for status in results)
print(f"requests={len(results)} admitted={admitted} rejected={len(results) - admitted} limit={10} window_seconds={10}")
