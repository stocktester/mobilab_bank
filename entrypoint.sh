#!/bin/bash

python wait_for_postgres.py && python manage.py migrate && python manage.py runserver 0.0.0.0:$SERVER_PORT
