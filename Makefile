build:
	pip install pipenv
	cd narad && pipenv install
migrations:
	cd narad && pipenv run python manage.py makemigrations
migrate:
	cd narad && pipenv run python manage.py migrate
run-webserver:
	cd narad && pipenv run python manage.py runserver
run-task-runner:
	cd narad && pipenv run celery -A narad worker -l info
docker-compose-run:
	docker-compose up --build
