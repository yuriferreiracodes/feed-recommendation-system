.PHONY: install lint format test run up down logs mysql migrate migration rollback

install:
	pip install -e ".[dev]"

lint:
	ruff check .

run:
	uvicorn backend.main:app --reload

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f backend

mysql:
	docker compose exec db mysql -uroot -proot feedapp

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(msg)"

rollback:
	alembic downgrade -1
