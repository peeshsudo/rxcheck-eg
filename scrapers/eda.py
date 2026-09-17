"""EDA (Egyptian Drug Authority) sync.

The EDA portal at eservices.edaegypt.gov.eg does not currently expose a
public API. Options:
  1. Request official API access from EDA
  2. Use the public search UI with careful rate-limiting
  3. Manual CSV imports maintained by a data operator
"""
import httpx
from scrapers.base import BaseScraper


class EDAScraper(BaseScraper):
    source = "EDA"
    BASE = "https://eservices.edaegypt.gov.eg"

    async def fetch_all(self) -> list[dict]:
        # Placeholder: replace with the real endpoint once EDA access is granted
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(f"{self.BASE}/api/drugs")
            if r.status_code != 200:
                return []
            return r.json()