#!/bin/bash

python /vpn/src/manage.py makemigrations
python /vpn/src/manage.py migrate

python /vpn/src/manage.py runserver 0:8000