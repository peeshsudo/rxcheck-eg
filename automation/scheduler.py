"""APScheduler-based cron replacement. Runs inside docker-compose."""
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Import your sync entrypoints
import sys
sys.path.insert(0, "/app")
from scrapers.sync_all import main as sync_all


async def run_sync():
    print("[scheduler] Starting full sync...")
    await sync_all()
    print("[scheduler] Sync complete.")


async def main():
    scheduler = AsyncIOScheduler()

    # FDA: 2 AM daily
    scheduler.add_job(run_sync, CronTrigger.from_crontab("0 2 * * *"), id="sync_all")

    # EMA: 3 AM daily (EMA itself updates twice daily)
    # Could split into two jobs if you want tighter freshness

    scheduler.start()
    print("[scheduler] Running. Jobs:", scheduler.get_jobs())

    # Keep the process alive
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())