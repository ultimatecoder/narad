#! /bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput
daphne -t 15 -b 0.0.0.0 -p $PORT narad.asgi:application
