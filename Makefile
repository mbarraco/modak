.PHONY: test

SERVICE_NAME=app

TEST_COMMAND=pytest

test:
	docker-compose run --rm $(SERVICE_NAME) $(TEST_COMMAND)
