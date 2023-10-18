install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install

update:
	poetry update

format:
	poetry run black wms tests
	poetry run ruff --fix wms tests

lint:
	poetry run black --check wms tests
	poetry run ruff check wms tests
	poetry run mypy wms tests

test:
	poetry run pytest --lf --cov
