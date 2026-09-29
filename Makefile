COMPOSE = docker compose -f harness/compose.yaml
.PHONY: up down contract load burst retry

# Three instances on 8091, 8092 and 8093, and Redis.
up:
	$(COMPOSE) up -d --build --wait redis api1 api2 api3

down:
	$(COMPOSE) down -v --remove-orphans

# What the API already does, black-box. Passes before and after your change.
contract:
	$(COMPOSE) run --rm --build contract

# 30 requests for one key, one at a time, round-robin across the three.
load:
	$(COMPOSE) run --rm --build tools python3 load.py

# 60 requests for one key at the same moment, 20 to each instance.
burst:
	$(COMPOSE) run --rm --build tools python3 burst.py

# Fill a key, read the 429's Retry-After, wait that long, try again.
retry:
	$(COMPOSE) run --rm --build tools python3 retry.py
