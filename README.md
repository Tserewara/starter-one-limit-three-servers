# The quota that multiplied

ParcelMint's quotes API as the team deployed it: three instances behind a
load balancer, and a Redis next to them. Each key is promised 10 requests per
10-second window. Each instance counts requests in its own memory.

```
service/    the quotes API: Python, with the redis client in requirements.txt
harness/    three instances of it, Redis, and the tools the drills use
contract/   black-box tests of what the API answers
```

## Run it

You need Docker with Compose, nothing else. `make up` starts the three
instances on `http://localhost:8091`, `:8092` and `:8093`, and Redis
(`redis://localhost:56379` from your machine, `redis://redis:6379/0` from the
instances, which read it as `REDIS_URL`). `curl
http://localhost:8091/health` tells you which instance answered. `make
contract` runs the contract tests, and `make down` removes the stack.

## API

`GET /v1/quotes` takes an `X-Api-Key` header and returns a small quote. Over
the limit it answers HTTP 429 with `{"error": "rate_limited", ...}`. `GET
/health` reports the instance name.

## Try the traffic

- `make load` sends 30 requests for one new key, one at a time,
  round-robin across the three instances, well inside one window (it takes
  a fraction of a second), and prints
  `requests=30 admitted=N rejected=N limit=10 window_seconds=10`.
- `make burst` sends 60 requests for one new key at the same moment, 20 to
  each instance, and prints `requests=60 concurrent admitted=N rejected=N
  limit=10`.
- `make retry` fills one new key round-robin across the three instances,
  reads the 429's `Retry-After` if there is one, waits that many seconds (the
  full 10 if there is none) and sends one more request. It prints the status
  and the header it saw, a line if it had to fall back to 10 seconds, and the
  status of the retry.

## Porting the service

The API is Python with the standard library; you can write it in another
language. It listens on port 8080 inside its container, reads `INSTANCE_ID`
and `REDIS_URL`, and answers the routes in `contract/openapi.yaml`. Build it
from `service/Dockerfile`, then run `make contract` until it passes.

## License

MIT. See `LICENSE`.
