#!/bin/sh
set -e

echo "Waiting for Postgres..."
until pg_isready -h database -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-database}"; do
  sleep 1
done
echo "Postgres is ready!"

echo "Running migrations with Django..."
python manage.py migrate
echo "Migrations complete!"

echo "Collecting statics..."
python manage.py collectstatic --no-input
echo "Statics collected!"

echo "Starting the Django server..."
exec gunicorn --bind "${BACKEND_HOST:-0.0.0.0}":"${BACKEND_PORT:-8000}" MeteoAnalyzer.wsgi:application