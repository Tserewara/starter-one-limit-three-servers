# The quota that multiplied

This is the ParcelMint quotes API used in the exercise. It runs three separate Python API containers beside a Redis container. Each instance starts with the behavior the team originally deployed.

## Run it

You need Docker with Compose. Start all three instances with:

```sh
make up
```

The instances are available at ports 8091, 8092, and 8093. Check one with `curl http://localhost:8091/health`. `make test` runs the given checks in a container, and `make down` removes the stack.

## Try the traffic shape

`make load` sends 30 requests with one API key, round-robin across all three instance URLs, and prints admitted requests, rejected requests, and the ten-second window. This is the same shape used to check the public quota.

## API

`GET /v1/quotes` accepts an `X-Api-Key` header and returns a small quote response. Requests over the local limit return JSON with HTTP 429 and a `Retry-After` header. `GET /health` reports the instance name.
