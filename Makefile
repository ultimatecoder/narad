build:
	pip install pipenv
	cd narad && pipenv install
migrations:
	cd narad && pipenv run python manage.py makemigrations
migrate:
	cd narad && pipenv run python manage.py migrate
run:
	cd narad && pipenv run python manage.py runserver
docker-compose-run:
	docker-compose up --build
