#!/bin/bash

# Stop on error
set -e

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting server..."
exec "$@"
