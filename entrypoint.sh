#!/bin/bash

python manage.py migrate && python manage.py flush --noinput && python manage.py loaddata "initial_data.json" &&
python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload
