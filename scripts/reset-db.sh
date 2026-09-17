#!/usr/bin/env bash
set -euo pipefail
docker-compose down -v
docker-compose up -d db
sleep 3
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.seed