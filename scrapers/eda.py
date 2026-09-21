"""EDA (Egyptian Drug Authority) sync — placeholder until API access is granted.

The EDA portal at eservices.edaegypt.gov.eg does not currently expose a
public API. Options:
  1. Request official API access from EDA (in progress)
  2. Use the public search UI with careful rate-limiting (ToS risk)
  3. Manual CSV imports maintained by a data operator

Until access is granted, this scraper returns an empty list. Data for EDA
comes from database/init/03_seed.sql (manual curation).
"""
from scrapers.base import BaseScraper


class EDAScraper(BaseScraper):
    source = "EDA"

    async def fetch_all(self) -> list[dict]:
        print("[EDA] No public API — skipping (see scrapers/eda.py docstring)")
        return []

    async def persist(self, records: list[dict]) -> int:
        # Nothing to persist until EDA API is available
        return 0