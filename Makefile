.PHONY: up down test load

export COMPOSE_PROJECT_NAME=three_servers

up:
	docker compose up -d --build redis api1 api2 api3

down:
	docker compose down -v --remove-orphans

test:
	docker compose run --rm --build test

load:
	docker compose run --rm --build loadgen
