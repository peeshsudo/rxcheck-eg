# RxCheck EG

Bilingual (Arabic/English) drug-interaction checker for Egyptian patients and pharmacists.

Syncs FDA, EMA, and EDA registries, promotes them to a canonical drug catalog, and lets patients build a personal medication schedule with timing and food-relation rules.

---

## Requirements

- Docker Engine 24+ and Docker Compose v2
- GNU/Linux, macOS, or WSL2 (Windows)
- ~4 GB free disk, ~2 GB RAM
- Python 3.12 (only if you want to run scripts outside Docker)

---

## Quick Start

```bash
git clone <your-repo> rxcheck-eg
cd rxcheck-eg

# 1. Create .env from the template
cp .env.example .env

# 2. Edit .env — set real values for:
#      POSTGRES_PASSWORD         (any strong string)
#      DATABASE_URL              (must use the SAME password above)
#      BACKEND_SECRET_KEY        (openssl rand -hex 32)
#      BACKEND_ADMIN_KEY         (openssl rand -hex 24)
nano .env

# 3. Make scripts executable
chmod +x scripts/*.sh

# 4. Run setup (builds images, starts services, waits for DB)
./scripts/setup.sh 2>&1 | tee setup.log
```

When the script finishes:

| Service | URL |
| :--- | :--- |
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/docs |
| Adminer (DB UI) | http://localhost:8080 |
| ChromaDB | http://localhost:8001 |

Open Adminer and log in with:
- **System**: PostgreSQL
- **Server**: db
- **Username**: your `POSTGRES_USER`
- **Password**: your `POSTGRES_PASSWORD`
- **Database**: your `POSTGRES_DB`

---

## Everyday Commands

```bash
docker-compose ps                       # what's running
docker-compose logs --tail=30 backend   # last 30 lines of backend
docker-compose restart backend          # reload after a code edit
docker-compose down                     # stop everything (keep data)
docker-compose down -v                  # stop AND wipe DB data
```

For the complete command reference, see `docs/docker-cheatsheet.md`.

---

## Data Sync

Scrapers run automatically at:

| Source | Cron (UTC) | Records per fetch |
| :--- | :--- | :--- |
| FDA | 02:00 | 100 |
| EMA | 03:00 | 500 (capped) |
| EDA | 04:00 | 0 (no public API) |

**Manual sync:**
```bash
docker-compose exec scheduler python -c "
import asyncio
from scrapers.sync_all import main
asyncio.run(main())"
```

**Promote staged records → canonical `drugs` / `products`:**
```bash
docker-compose exec scheduler python /app/scripts/promote_changes.py
```

**Or add the promoter to your daily sync** by editing `automation/scheduler.py` to include a `promote` job 1 hour after the scrapers.

---

## Project Layout

```
rxcheck-eg/
├── docker-compose.yml            service definitions
├── .env                          secrets (never commit)
├── backend/                      FastAPI app
│   ├── Dockerfile
│   └── app/
│       ├── main.py               app entrypoint
│       ├── config.py             env validation
│       ├── database.py           SQLAlchemy async engine
│       ├── models.py             ORM tables
│       ├── schemas.py            Pydantic DTOs
│       ├── security.py           middleware + admin key
│       └── routers/              one file per resource
├── automation/                   APScheduler container
│   └── scheduler.py
├── scrapers/                     shared scraper library
│   ├── base.py  fda.py  ema.py  eda.py  sync_all.py
├── frontend/                     Next.js App Router
│   ├── app/
│   └── components/
├── database/
│   └── init/                     SQL run on fresh volume
│       ├── 01_extensions.sql
│       ├── 02_schema.sql
│       └── 03_seed.sql
├── scripts/
│   ├── setup.sh                  first-time bootstrap
│   ├── reset-db.sh
│   └── promote_changes.py        staging → canonical promoter
└── docs/
    ├── architecture.md
    ├── data-sources.md
    └── docker-cheatsheet.md
```

---

## What each service does

| Service | Image | Purpose |
| :--- | :--- | :--- |
| `db` | `pgvector/pgvector:pg16` | Postgres + vector extension |
| `backend` | built from `backend/` | FastAPI, uvicorn, port 8000 |
| `frontend` | built from `frontend/` | Next.js dev server, port 3000 |
| `scheduler` | built from `automation/` | APScheduler — runs scrapers on cron |
| `chromadb` | `chromadb/chroma` | Vector store for AI agent |
| `adminer` | `adminer` | DB web UI on port 8080 |

---

## Troubleshooting

**`WARN: POSTGRES_USER is not set`**
Run `docker-compose` from the project root, or add the `dc` alias from `docs/docker-cheatsheet.md`.

**Backend crashes with `ModuleNotFoundError`**
A dependency was added to `requirements.txt` but the image wasn't rebuilt:
```bash
docker-compose build backend
docker-compose up -d --force-recreate backend
```

**Frontend 500 with `Module not found: Can't resolve '@/...'`**
Clear the Next.js cache and restart:
```bash
rm -rf frontend/.next
docker-compose restart frontend
```

**`email-validator is not installed`**
Add it and rebuild:
```bash
grep -q email-validator backend/requirements.txt || echo email-validator >> backend/requirements.txt
docker-compose build backend
docker-compose up -d --force-recreate backend
```

**`extension "vector" is not available`**
Wrong Postgres image. Must be `pgvector/pgvector:pg16`, not `postgres:16-alpine`.

**Root-owned files after a container write**
```bash
sudo chown -R $USER:$USER .
```
Then verify `scripts/setup.sh` exports `HOST_UID` / `HOST_GID`.

---

## Development

**Backend hot-reload** is on — save a `.py` file and uvicorn restarts automatically.

**Frontend** uses Next.js with webpack. On first load after a restart, expect 20–60 s of compile time. Subsequent requests are fast.

**Database schema changes:**
- For dev iteration: `docker-compose exec db psql -U rxcheck -d rxcheck -c "ALTER TABLE ..."`
- For permanence: edit `database/init/02_schema.sql` (only runs on a fresh volume)
- For a proper migration workflow: add Alembic

**Run tests:**
```bash
docker-compose exec backend pytest ../tests/backend -v
```

---

## Safety Notes

- Never commit `.env` — it holds DB passwords and API keys.
- The AI agent endpoints are for educational purposes only. They do not replace professional medical advice.

---

## License

See `LICENSE.txt`.