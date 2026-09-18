#!/usr/bin/env bash
set -euo pipefail

# Export UID/GID so containers run as your user (prevents root-owned files)
export UID="${UID:-$(id -u)}"
export GID="${GID:-$(id -g)}"

echo "→ Copying .env..."
[ -f .env ] || cp .env.example .env

echo "→ Building containers..."
docker-compose build

echo "→ Starting services..."
docker-compose up -d

echo "→ Waiting for DB..."
sleep 5

echo "→ Running migrations..."
docker-compose exec backend alembic upgrade head #|| true "commented to know when migrations fail."

echo "→ Seeding..."
docker-compose exec backend python -m app.seed #|| true "commented to know when migrations fail."

echo "✅ Ready. Frontend: http://localhost:3000  API: http://localhost:8000/docs"