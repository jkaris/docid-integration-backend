#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z docid-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"


python manage.py recreate_db
gunicorn -w 4 -b 0.0.0.0:5000 docid_app.wsgi:app
