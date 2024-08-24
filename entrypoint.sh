#!/bin/bash

# Apply database migrations
conda run --name InfinityVision python manage.py migrate

# Collect static files
conda run --name InfinityVision python manage.py collectstatic --noinput

# Start the application using Gunicorn
exec conda run --name InfinityVision gunicorn InfinityVision.wsgi:application --bind 0.0.0.0:8000
