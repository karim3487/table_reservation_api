.PHONY: build up down migrate tests run-tests-docker test-db-up test-db-down

build:
	docker-compose build

up:
	docker-compose --env-file .env.prod up -d db
	ENV=prod docker-compose --env-file .env.prod up -d web

down:
	docker-compose down

migrate:
	docker-compose exec -e ENV=prod web uv run alembic upgrade head

# 🧪 Run tests inside Docker
run-tests-docker:
	ENV=test docker-compose run --rm web uv run pytest -v --tb=short

# 🔄 Test DB only (PostgreSQL)
test-db-up:
	docker-compose --env-file .env.test up -d test-db

test-db-down:
	docker-compose stop test-db
