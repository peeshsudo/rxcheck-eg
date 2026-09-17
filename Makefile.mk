.PHONY: install dev stop test lint migrate seed sync

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python -m app.seed

sync:
	docker-compose exec backend python -m scrapers.sync_all

test:
	cd backend && pytest
	cd frontend && npm test

lint:
	cd backend && ruff check . && mypy app
	cd frontend && npm run lint
