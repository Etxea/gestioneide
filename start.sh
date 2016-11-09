#!/bin/bash

# Start Gunicorn processes
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

echo Starting Gunicorn.
exec gunicorn gestioneide.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
