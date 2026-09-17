"""Runs all scrapers, writes change_events to the DB."""
import asyncio
from scrapers.fda import FDAScraper
from scrapers.ema import EMAScraper
from scrapers.eda import EDAScraper
from app.config import settings


async def run_source(scraper):
    print(f"→ Syncing {scraper.source}...")
    try:
        records = await scraper.run()
        print(f"  ✓ {scraper.source}: {len(records)} records")
    except Exception as e:
        print(f"  ✗ {scraper.source} failed: {e}")


async def main():
    await asyncio.gather(
        run_source(FDAScraper(settings.openfda_api_key)),
        run_source(EMAScraper()),
        run_source(EDAScraper()),
    )


if __name__ == "__main__":
    asyncio.run(main())