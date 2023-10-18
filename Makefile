install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install

update:
	poetry update

format:
	poetry run black firstlib tests
	poetry run ruff --fix firstlib tests

lint:
	poetry run black --check firstlib tests
	poetry run ruff check firstlib tests
	poetry run mypy firstlib tests

test:
	poetry run pytest --lf --cov

unit-test-ci:
	poetry run pytest tests/unit
