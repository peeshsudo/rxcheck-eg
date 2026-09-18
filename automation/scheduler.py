"""APScheduler-based cron replacement. Runs inside docker-compose."""
import asyncio
import os
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

sys.path.insert(0, "/app")

from scrapers.sync_all import main as sync_all


async def run_sync():
    print("[scheduler] Starting full sync...")
    result = sync_all()
    if asyncio.iscoroutine(result):
        await result
    print("[scheduler] Sync complete.")


async def main():
    scheduler = AsyncIOScheduler()

    # FDA: 2 AM daily
    scheduler.add_job(run_sync, CronTrigger.from_crontab(os.getenv("SYNC_FDA_CRON", "0 2 * * *")), id="sync_fda")
    # EMA: 3 AM daily
    scheduler.add_job(run_sync, CronTrigger.from_crontab(os.getenv("SYNC_EMA_CRON", "0 3 * * *")), id="sync_ema")
    # EDA: 4 AM daily
    scheduler.add_job(run_sync, CronTrigger.from_crontab(os.getenv("SYNC_EDA_CRON", "0 4 * * *")), id="sync_eda")

    scheduler.start()
    #print("[scheduler] Running. Jobs:", scheduler.get_jobs())

    print("[scheduler] Running. Jobs:")
    for job in scheduler.get_jobs():
        print(f"  - {job.id}: {job.trigger}")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())