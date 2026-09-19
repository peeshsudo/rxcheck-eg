"""
file scrapers/ema.py
EMA medicines sync.

Changes from prior version:
- Replaced HTML landing page with real JSON endpoints
  (verified: /en/media/67423 = medicines, /en/media/67425 = documents)
- Added graceful handling of non-JSON responses
- Added retry with exponential backoff
"""
import asyncio
import httpx

from app.config import settings
from scrapers.base import BaseScraper


class EMAScraper(BaseScraper):
    source = "EMA"

    def __init__(
        self,
        medicines_url: str | None = None,
        documents_url: str | None = None,
        max_retries: int = 3,
    ):
        self.medicines_url = medicines_url or settings.ema_medicines_json_url
        self.documents_url = documents_url or settings.ema_documents_json_url
        self.max_retries = max_retries

    async def _fetch_json(self, url: str) -> list[dict]:
        """Fetch JSON with retries. Returns the list payload. Raises on non-JSON responses."""
        delay = 1.0
        last_err: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                    r = await client.get(
                        url,
                        headers={"Accept": "application/json"},
                    )
                    r.raise_for_status()

                    content_type = r.headers.get("content-type", "")
                    if "json" not in content_type.lower():
                        raise ValueError(
                            f"Expected JSON from {url}, got {content_type!r}. "
                            f"EMA may have moved the file — check "
                            f"docs/data-sources.md for the current URL."
                        )
                    #return r.json()
                    data = r.json()

                    # EMA wraps records in a top-level object
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict):
                        # Try common wrappers in order
                        for key in ("data", "results", "items", "medicines", "documents"):
                            if key in data and isinstance(data[key], list):
                                return data[key]
                        # Fallback: first list value found
                        for v in data.values():
                            if isinstance(v, list):
                                return v
                        # No list at all — return empty rather than crash
                        return []
                    return []
            except Exception as e:
                last_err = e
                if attempt < self.max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2

        raise RuntimeError(f"EMA fetch failed after {self.max_retries} tries: {last_err}")

    async def fetch_all(self) -> list[dict]:
        """Pull both EMA JSON bundles."""
        medicines = await self._fetch_json(self.medicines_url)
        documents = await self._fetch_json(self.documents_url)
        return medicines + documents