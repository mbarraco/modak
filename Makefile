.PHONY: test build down bash restart run-cli

SERVICE_NAME=app
TEST_COMMAND=pytest -s

test:
	docker compose run --rm $(SERVICE_NAME) $(TEST_COMMAND)

build:
	docker compose build

down:
	docker compose down

bash:
	docker compose run --rm $(SERVICE_NAME) /bin/bash

restart:
	docker compose restart

run-cli:
	@echo "Running cli.py in a new Docker container..."
	@docker compose run --rm -it app python /code/cli.py

