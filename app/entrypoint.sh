#!/bin/bash
sleep 5
python manage.py makemigrations
python manage.py migrate
exec gunicorn car_sharing_project.wsgi:application --bind 0.0.0.0:8000 --reload
