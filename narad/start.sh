#! /bin/sh

pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
pipenv run daphne -t 15 -b 0.0.0.0 -p 8000 narad.asgi:application
