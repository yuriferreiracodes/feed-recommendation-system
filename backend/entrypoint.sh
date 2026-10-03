#!/bin/sh
# Apply pending migrations before serving, so a fresh `docker compose up`
# yields a usable schema without a manual `alembic upgrade head`.
set -e

echo "Running database migrations..."
alembic upgrade head

exec "$@"
