# RxCheck EG — Docker Command Cheat Sheet

All commands assume you are in the project root:

    cd ~/Documents/rxcheck-eg

To avoid the `WARN: POSTGRES_USER is not set` warnings, always run from
the project root, OR add this alias to `~/.bashrc`:

    alias dc='docker-compose -f ~/Documents/rxcheck-eg/docker-compose.yml --env-file ~/Documents/rxcheck-eg/.env'

Then use `dc` instead of `docker-compose` from anywhere.

---

## 🚀 1. FIRST-TIME SETUP (run once)

    # Build all Docker images (backend, frontend, scheduler)
    docker-compose build

    # Start the full stack in the background
    docker-compose up -d

    # Verify all 6 containers are running
    docker-compose ps

    # Wait ~30s for Postgres to initialize, then check
    docker-compose logs --tail=30 db

    # Open the app
    #   Frontend: http://localhost:3000
    #   API docs: http://localhost:8000/docs
    #   Adminer:  http://localhost:8080
    #   Chroma:   http://localhost:8001

---

## 🔧 2. DAILY COMMANDS — Start / Stop / Restart

    # Start the whole stack (creates containers if missing)
    docker-compose up -d

    # Stop the whole stack but KEEP data (volumes survive)
    docker-compose stop

    # Start again after stop
    docker-compose start

    # Restart the whole stack (keeps containers, restarts processes)
    docker-compose restart

    # Bring everything down (containers removed, data still safe)
    docker-compose down

    # ⚠️ DESTRUCTIVE: bring down AND delete all volumes
    #    → wipes Postgres data, Chroma vectors, and re-runs init SQL
    docker-compose down -v

---

## 🔄 3. RESTART ONE SERVICE (without touching others)

    # Restart backend only (useful after editing app/*.py)
    docker-compose restart backend

    # Restart frontend only (useful after editing tsconfig.json)
    docker-compose restart frontend

    # Restart scheduler only (useful after editing scrapers/*.py or base.py)
    docker-compose restart scheduler

    # Rebuild + recreate ONE service (needed when requirements.txt changes
    # or when Dockerfile changed)
    docker-compose up -d --force-recreate backend
    docker-compose up -d --force-recreate frontend
    docker-compose up -d --force-recreate scheduler

    # 🎯 The golden rule:
    #   - Python/TS file change          → `restart`
    #   - requirements.txt / Dockerfile  → `build` + `up -d --force-recreate`
    #   - docker-compose.yml change      → `down` + `up -d`
    #   - .env change                    → `up -d --force-recreate <svc>`

---

## 📜 4. VIEW LOGS

    # ⚠️ `-f` means FOLLOW — hangs forever. Always Ctrl+C to exit.
    # For diagnostics, prefer `--tail=N` WITHOUT `-f`.

    # Show last 30 lines then exit (use this for troubleshooting)
    docker-compose logs --tail=30 backend
    docker-compose logs --tail=30 frontend
    docker-compose logs --tail=30 scheduler
    docker-compose logs --tail=30 db

    # Follow logs live (for watching in real time)
    docker-compose logs -f scheduler
    docker-compose logs -f backend

    # Follow all services at once
    docker-compose logs -f

    # Filter logs for errors only
    docker-compose logs --tail=100 backend | grep -iE "error|traceback|exception"

    # Save logs to file for sharing
    docker-compose logs --tail=200 scheduler > setup.log 2>&1

---

## 🐘 5. DATABASE — Access & Inspect

    # Open an interactive psql shell inside the db container
    docker-compose exec db psql -U rxcheck -d rxcheck

    # List all tables
    docker-compose exec db psql -U rxcheck -d rxcheck -c "\dt"

    # Describe one table (columns, indexes, constraints)
    docker-compose exec db psql -U rxcheck -d rxcheck -c "\d drugs"
    docker-compose exec db psql -U rxcheck -d rxcheck -c "\d schedules"

    # Row counts across all tables
    docker-compose exec db psql -U rxcheck -d rxcheck -c "
    SELECT 'drugs' AS t, COUNT(*) FROM drugs
    UNION ALL SELECT 'products', COUNT(*) FROM products
    UNION ALL SELECT 'interactions', COUNT(*) FROM interactions
    UNION ALL SELECT 'change_events', COUNT(*) FROM change_events
    UNION ALL SELECT 'schedules', COUNT(*) FROM schedules
    UNION ALL SELECT 'sync_state', COUNT(*) FROM sync_state;"

    # Sync health check (per-source, last run, errors)
    docker-compose exec db psql -U rxcheck -d rxcheck -c "
    SELECT source, records_synced, last_success_at, last_error
    FROM sync_state ORDER BY source;"

    # Is Postgres ready to accept connections?
    docker-compose exec db pg_isready -U rxcheck

    # Backup database to a file
    docker-compose exec db pg_dump -U rxcheck rxcheck > backup_$(date +%Y%m%d).sql

    # Restore from a backup
    docker-compose exec -T db psql -U rxcheck -d rxcheck < backup_YYYYMMDD.sql

---

## 🕷️ 6. SCRAPERS — Manual Syncs (bypassing cron)

    # Run ALL scrapers immediately (FDA + EMA + EDA)
    docker-compose exec scheduler python -c "
    import asyncio
    from scrapers.sync_all import main
    asyncio.run(main())"

    # Test ONLY the FDA scraper
    docker-compose exec scheduler python -c "
    import asyncio
    from scrapers.fda import FDAScraper
    async def t():
        s = FDAScraper()
        print(f'FDA: {len(await s.run())} records')
    asyncio.run(t())"

    # Test ONLY the EMA scraper
    docker-compose exec scheduler python -c "
    import asyncio
    from scrapers.ema import EMAScraper
    async def t():
        s = EMAScraper()
        print(f'EMA: {len(await s.run())} records')
    asyncio.run(t())"

    # Syntax-check all scraper files (no container needed)
    for f in scrapers/*.py; do python3 -m py_compile "$f" && echo "✅ $f"; done

---

## 🩺 7. HEALTH CHECKS

    # Are all 6 containers up?
    docker-compose ps

    # Backend API alive?
    curl -s --max-time 10 http://localhost:8000/health

    # Frontend alive?
    curl -s --max-time 60 -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3000

    # Backend docs page reachable?
    curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/docs

    # Drug search working?
    curl -s --max-time 10 "http://localhost:8000/api/v1/drugs/search?q=aspirin"

    # Full list of registered API routes
    curl -s http://localhost:8000/openapi.json | python3 -c "
    import json, sys
    for p in sorted(json.load(sys.stdin)['paths']): print(p)"

    # Scheduled cron jobs list
    docker-compose logs scheduler | grep -E "sync_(fda|ema|eda)"

---

## 🧹 8. DEEP CLEAN & RESET

    # Stop everything, remove containers, KEEP data
    docker-compose down

    # Stop everything, remove containers, DELETE data (fresh start)
    # ⚠️ Postgres will re-run database/init/*.sql on next `up -d`
    docker-compose down -v

    # Nuclear option: remove images too (rebuild from scratch next time)
    docker-compose down -v --rmi all

    # Prune Docker's cache (frees disk, doesn't touch your project)
    docker system prune -f

    # Check disk usage
    docker system df

---

## 🔍 9. TROUBLESHOOTING — Common Issues

    # Issue: "column X does not exist" in DB → add missing column
    #   (see log for exact column name)
    docker-compose exec db psql -U rxcheck -d rxcheck -c "
    ALTER TABLE drugs ADD COLUMN IF NOT EXISTS unii VARCHAR(20);"

    # Issue: "ModuleNotFoundError" → rebuild that service
    docker-compose build backend
    docker-compose up -d --force-recreate backend

    # Issue: "ImportError: cannot import name X" → check the module file
    cat backend/app/database.py       # look for actual name
    grep -rn "from app" backend/app/  # find all imports

    # Issue: "SyntaxError: invalid syntax" → check the file
    python3 -m py_compile scrapers/eda.py

    # Issue: scheduler container is "Up" but no logs
    #   → Python is buffering stdout. Apply `python -u` + PYTHONUNBUFFERED=1.
    #   → Verify with: `docker-compose stop scheduler && docker-compose logs scheduler`
    #   (on SIGTERM, buffer flushes and you'll see all buffered prints at once)

    # Issue: Postgres exits with code 3 on startup
    docker-compose logs --tail=40 db      # look for "extension ... not available"
    # → usually means wrong image. Must be: pgvector/pgvector:pg16

    # Issue: "root-owned files" after container writes
    find . -user root -not -path "./frontend/node_modules/*" -not -path "./.git/*"
    sudo chown -R $USER:$USER .
    # → permanent fix: HOST_UID/HOST_GID in docker-compose + setup.sh

    # Issue: frontend 500 "Module not found: Can't resolve '@/...'"
    #   → verify tsconfig.json has baseUrl + paths
    grep -E "baseUrl|paths" frontend/tsconfig.json
    #   → clear cache and restart
    sudo rm -rf frontend/.next
    docker-compose restart frontend

---

## 📋 10. THE STANDARD FLOW AFTER EDITING CODE

    # 1. Edited Python in backend/app/? → restart backend
    docker-compose restart backend

    # 2. Edited a scraper or scheduler.py? → restart scheduler
    docker-compose restart scheduler

    # 3. Edited TypeScript/React in frontend/? → Next.js hot-reloads,
    #    but if it doesn't, clear cache + restart:
    sudo rm -rf frontend/.next
    docker-compose restart frontend

    # 4. Changed requirements.txt or Dockerfile? → rebuild
    docker-compose build backend
    docker-compose up -d --force-recreate backend

    # 5. Changed .env? → recreate the services that read it
    docker-compose up -d --force-recreate backend scheduler

    # 6. Changed database/init/*.sql? → SQL only runs on FRESH volume
    docker-compose down -v
    docker-compose up -d

    # 7. Verify everything is still OK
    docker-compose ps
    curl -s -o /dev/null -w "Backend: %{http_code}\n" http://localhost:8000/health
    curl -s -o /dev/null -w "Frontend: %{http_code}\n" --max-time 60 http://localhost:3000

---

## 🗂️ 11. PROJECT STRUCTURE (for reference)

    rxcheck-eg/
    ├── docker-compose.yml          ← service definitions
    ├── .env                        ← secrets (never commit)
    ├── .env.example                ← template
    ├── backend/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/                    ← FastAPI code
    ├── automation/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── scheduler.py            ← APScheduler entrypoint
    ├── frontend/
    │   ├── Dockerfile
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── app/                    ← Next.js App Router
    │   └── components/             ← ScanFlow, TimeSelector, etc.
    ├── scrapers/                   ← shared library
    │   ├── base.py
    │   ├── fda.py
    │   ├── ema.py
    │   ├── eda.py
    │   └── sync_all.py
    ├── database/
    │   └── init/                   ← runs on fresh volume
    │       ├── 01_extensions.sql
    │       ├── 02_schema.sql
    │       └── 03_seed.sql
    └── scripts/
        └── setup.sh

---

## 🎯 12. THE ONE-LINER YOU'LL USE MOST

    # From project root — the "is everything OK?" check
    docker-compose ps && \
    curl -s -o /dev/null -w "backend=%{http_code} " http://localhost:8000/health && \
    curl -s --max-time 60 -o /dev/null -w "frontend=%{http_code}\n" http://localhost:3000

    # Expected output:
    #   ... 6 containers all "Up" ...
    #   backend=200 frontend=200

    # All tables with sizes
sudo docker-compose exec db psql -U rxcheck -d rxcheck -c "
SELECT schemaname, relname, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;"

# What's actually in change_events
sudo docker-compose exec db psql -U rxcheck -d rxcheck -c "
SELECT source, entity_type, change_type, COUNT(*)
FROM change_events
GROUP BY source, entity_type, change_type;"

# Sync health
sudo docker-compose exec db psql -U rxcheck -d rxcheck -c "
SELECT source, records_synced, last_success_at, last_error FROM sync_state;"

# What products exist (this is why /products/search returns [])
sudo docker-compose exec db psql -U rxcheck -d rxcheck -c "
SELECT p.market, p.brand_en, p.brand_ar, d.generic_en
FROM products p JOIN drugs d ON d.id = p.drug_id;"

# Peek at one change_event payload
sudo docker-compose exec db psql -U rxcheck -d rxcheck -c "
SELECT source, external_id, LEFT(raw_payload::text, 200)
FROM change_events LIMIT 3;"