#!/bin/bash

# Source conda.sh to enable conda commands
source /opt/conda/etc/profile.d/conda.sh

# Activate the conda environment
conda activate InfinityVision

# Set the Python path
export PYTHONPATH=/app/InfinityVision

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

export DJANGO_SETTINGS_MODULE=InfinityVision.settings

# Start the application using Gunicorn
exec gunicorn --workers=2 InfinityVision.wsgi:application --bind 0.0.0.0:8000
