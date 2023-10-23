help:
	python -m firstlib.runner --help

install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install

lock:
	poetry lock --no-update

update:
	poetry update

format:
	poetry run black firstlib tests
	poetry run ruff --fix firstlib tests

lint:
	poetry run black --check firstlib tests
	poetry run ruff check firstlib tests
	poetry run mypy firstlib tests

amend:
	git commit --amend --no-edit -a

test:
	poetry run pytest --lf --cov

unit-test-ci:
	poetry run pytest tests/unit

run:
	python -m pos.runner --host localhost --port 8000
