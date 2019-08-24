migrations:
	pipenv run python narad/manage.py makemigrations
migrate:
	pipenv run python narad/manage.py migrate
