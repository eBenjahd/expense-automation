#!/bin/sh
set -e

echo "Esperando a que Postgres esté listo..."
until pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
  echo "Postgres no está listo aún, esperando..."
  sleep 2
done

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn expense.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -