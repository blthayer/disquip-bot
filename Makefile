SHELL := /bin/bash

no_op:
	@echo "Doing nothing but printing this message!"

install_packages:
	poetry install --verbose --sync

install: install_packages
	poetry run pre-commit install --install-hooks

test:
	poetry run pytest tests disquip_bot .

format:
	poetry run isort .
	poetry run autoflake --in-place --recursive .
	poetry run black .

lint:
	poetry run flake8 --max-line-length 79 --ignore=E203,W503 disquip_bot
	poetry run pylint disquip_bot tests

standards: format test lint
