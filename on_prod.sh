#!/bin/bash
export DJANGO_SETTINGS_MODULE=lonelygourmet.settings.prod
python3 manage.py runserver 0.0.0.0:8080
