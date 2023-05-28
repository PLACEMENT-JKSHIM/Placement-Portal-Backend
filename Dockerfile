FROM python:3.10-alpine3.17 as web

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && apk add --no-cache mariadb-connector-c-dev build-base nginx openrc

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

RUN chmod +x ./createsuperuser.sh
RUN ./createsuperuser.sh

EXPOSE 80


COPY nginx.conf /etc/nginx/http.d/default.conf
RUN mkdir /var/log/gunicorn/
RUN nginx

CMD  nginx && gunicorn --bind 0.0.0.0:8000 main.wsgi:application -w 3 --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log


