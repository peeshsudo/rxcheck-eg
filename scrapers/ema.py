"""EMA medicines sync. EMA publishes JSON twice daily (06:00, 18:00 CET)."""
import httpx
from scrapers.base import BaseScraper


class EMAScraper(BaseScraper):
    source = "EMA"
    # Real endpoint: https://www.ema.europa.eu/en/documents/report/...
    BASE = "https://www.ema.europa.eu/en/medicines/download-medicine-data"

    async def fetch_all(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(self.BASE)
            r.raise_for_status()
            # EMA actually returns an Excel/JSON bundle — parse accordingly
            return []