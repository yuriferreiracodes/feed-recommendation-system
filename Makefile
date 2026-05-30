.PHONY: run test lint install

run:
	uvicorn backend.main:app --reload

test:
	pytest -v

lint:
	ruff check . && mypy backend

install:
	pip install -e ".[dev]"
