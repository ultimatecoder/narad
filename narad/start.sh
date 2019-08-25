#! /bin/sh

pipenv run python manage.py migrate --noinput
#pipenv run python manage.py collectstatic --noinput
pipenv run gunicorn --bind 0.0.0.0:8000 -t $WEBTIMEOUT narad.wsgi:application
