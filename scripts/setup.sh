#!/usr/bin/env bash
set -euo pipefail

# Export host UID/GID so containers run as your user (prevents root-owned files)
# Note: bash's UID/GID are readonly, so we use HOST_UID/HOST_GID
export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"

echo "→ Copying .env..."
[ -f .env ] || cp .env.example .env

echo "→ Building containers..."
docker-compose build

echo "→ Starting services..."
docker-compose up -d

echo "→ Waiting for DB to initialize..."
until docker compose exec -T db pg_isready -U "${POSTGRES_USER:-rxcheck}" >/dev/null 2>&1; do
  echo "   ...waiting"
  sleep 2
done

#echo "→ Running migrations..."
#docker-compose exec backend alembic upgrade head #|| true "commented to know when migrations fail."

#echo "→ Seeding..."
#docker-compose exec backend python -m app.seed #|| true "commented to know when migrations fail."

echo "✅ Ready. Frontend: http://localhost:3000  API: http://localhost:8000/docs"