.PHONY: black test build down bash restart run-cli

APP_SERVICE_NAME=app
TEST_COMMAND=pytest -s
PERF_TEST_COMMAND=python performance_test.py
BLACK_COMMAND=black .


black:
	docker compose run --rm $(APP_SERVICE_NAME) $(BLACK_COMMAND)

test:
	docker compose run --rm $(APP_SERVICE_NAME) $(TEST_COMMAND)

build:
	docker compose build

down:
	docker compose down

bash:
	docker compose run --rm $(APP_SERVICE_NAME) /bin/bash

restart:
	docker compose restart

run-cli:
	@echo "Running cli.py in a new Docker container..."
	@docker compose run --rm -it app python /code/cli.py

run-perf-test:
	@echo "Running performance tests..."
	@docker compose run --rm $(APP_SERVICE_NAME) $(PERF_TEST_COMMAND)