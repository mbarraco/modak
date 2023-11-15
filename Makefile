.PHONY: test build down bash restart

SERVICE_NAME=app
TEST_COMMAND=pytest

test:
	docker-compose run --rm $(SERVICE_NAME) $(TEST_COMMAND)

build:
	docker-compose build

down:
	docker-compose down

bash:
	docker-compose run --rm $(SERVICE_NAME) /bin/bash

restart:
	docker-compose restart
