FROM python:latest

ENV STATIC_ROOT /srv/www/static

WORKDIR /srv/www/app

COPY uploads uploads

RUN pip install pipenv

COPY manage.py .

COPY Pipfile .

COPY Pipfile.lock .

RUN pipenv install

COPY narad narad

COPY product_manager product_manager

COPY start.sh .

CMD bash start.sh
