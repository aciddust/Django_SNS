#!/bin/bash
export DJANGO_SETTINGS_MODULE=lonelygourmet.settings.dev
python manage.py runserver 0.0.0.0:8080
