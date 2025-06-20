test:
	pytest

coverage:
	pytest -s --cov --cov-report html --cov-fail-under 100

server:
	python main.py

lint:
	pylint $(shell git ls-files '*.py')