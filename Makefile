build:
	docker-compose build

migrate:
	docker-compose run --rm app ./wait-for-it.sh -t 60 postgres:5432 -- \
		python -c "from src.db.manager import setup_database; setup_database()"

run:
	docker-compose up

setup: build migrate

test:
	docker-compose run --rm app pytest
