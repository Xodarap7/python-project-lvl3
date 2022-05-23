build:
	rm -rf dist
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader tests

test:
	poetry run pytest -vv page_loader tests

install:
	poetry install

start:
	rm -rf site/*
	poetry run python3 -m page_loader.scripts.loader -o site 'https://www.rydlab.ru'

test_log:
	poetry run pytest -o log_cli=true\
 	--log-cli-level=debug\
 	page_loader tests