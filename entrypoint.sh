#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
python - <<'PY'
import os
import time

import psycopg

for _ in range(30):
    try:
        psycopg.connect(
            host=os.environ.get("POSTGRES_HOST", "db"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
            dbname=os.environ.get("POSTGRES_DB", "articles_db"),
            user=os.environ.get("POSTGRES_USER", "articles_user"),
            password=os.environ.get("POSTGRES_PASSWORD", "articles_password"),
        ).close()
        break
    except Exception:
        time.sleep(2)
else:
    raise SystemExit("Database is unavailable")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${LOAD_INITIAL_DATA:-${LOAD_DEMO_DATA:-False}}" = "True" ]; then
    python manage.py seed_initial_data
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
