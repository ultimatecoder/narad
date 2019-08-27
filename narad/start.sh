#! /bin/sh

pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
pipenv run daphne -b 0.0.0.0 -p 8000 narad.asgi:application
