#!/usr/bin/env bash
set -euo pipefail

echo "→ Copying .env..."
[ -f .env ] || cp .env.example .env

echo "→ Building containers..."
docker-compose build

echo "→ Starting services..."
docker-compose up -d

echo "→ Waiting for DB..."
sleep 5

echo "→ Running migrations..."
docker-compose exec backend alembic upgrade head || true

echo "→ Seeding..."
docker-compose exec backend python -m app.seed || true

echo "✅ Ready. Frontend: http://localhost:3000  API: http://localhost:8000/docs"