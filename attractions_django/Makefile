test:
	python manage.py test

coverage:
	coverage run --source='.' manage.py test
	coverage html
	coverage report --fail-under=100

server:
	python manage.py runserver

lint:
	pylint $(shell git ls-files '*.py')