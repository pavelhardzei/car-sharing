#!/bin/bash
sleep 15
python manage.py makemigrations
python manage.py migrate
