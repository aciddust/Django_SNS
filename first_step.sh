#!/bin/bash
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py makemigrations contents
python manage.py migrate
python manage.py createsuperuser

