#!/bin/bash

python /vpn/src/manage.py makemigrations
python /vpn/src/manage.py migrate

python /vpn/src/manage.py collectstatic --noinput

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src config.wsgi:application --reload --log-level=${WSGI_LOG_LEVEL}