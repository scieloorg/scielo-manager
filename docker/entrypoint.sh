#!/usr/bin/env sh
set -eu

echo "Waiting for PostgreSQL at ${DB_HOST:-db}:${DB_PORT:-5432}..."
until python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('${DB_HOST:-db}', int('${DB_PORT:-5432}'))); s.close()" 2>/dev/null; do
  sleep 1
done

echo "PostgreSQL is up."

python3 scielomanager/manage.py migrate --settings=scielomanager.settings || true

if [ "$#" -eq 0 ]; then
  set -- python3 scielomanager/manage.py runserver 0.0.0.0:8000
fi

exec "$@"
