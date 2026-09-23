# The quota that multiplied

This is ParcelMint's quotes API as the team deployed it: three Python API containers next to a Redis container. Each instance counts requests in its own memory.

## Run it

You need Docker with Compose. `make up` starts the three instances on ports 8091, 8092 and 8093, and `curl http://localhost:8091/health` tells you which one answered. `make test` runs the given checks in a container, and `make down` removes the stack.

## Try the traffic

`make load` sends 30 requests with one API key, round-robin across the three instances, and prints one line with the requests, how many were admitted and rejected, the limit and the window. It's the same traffic the quota is checked against.

## API

`GET /v1/quotes` takes an `X-Api-Key` header and returns a small quote. Over the local limit it answers HTTP 429 with a JSON body. `GET /health` reports the instance name.
