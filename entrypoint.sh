#!/bin/bash

python wait_for_postgres.py && python manage.py migrate && gunicorn