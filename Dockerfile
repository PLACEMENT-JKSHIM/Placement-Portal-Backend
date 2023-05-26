FROM python:3.10-alpine3.17

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && apk add --no-cache mariadb-connector-c-dev build-base

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

RUN ./createsuperuser.sh

EXPOSE 8000



CMD python manage.py runserver 0.0.0.0:8000
