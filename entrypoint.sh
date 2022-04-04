#!/bin/bash

python manage.py migrate &&
(if [ -z "$POPULATE_DB" ]; then echo "Skipping db population."; else
echo "Flushing database" &&
python manage.py flush --noinput &&
echo "Populating Database" &&
python manage.py loaddata "initial_data.json";fi) &&
echo "Getting server ready..." &&
python manage.py runserver 0.0.0.0:"$SERVER_PORT" --noreload
