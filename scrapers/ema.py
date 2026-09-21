"""EMA medicines sync — pulls JSON bundles from ema.europa.eu."""
import asyncio
import json
import httpx
from sqlalchemy import text

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
        """Fetch JSON with retries. Returns the list payload."""
        delay = 1.0
        last_err: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                    r = await client.get(url, headers={"Accept": "application/json"})
                    r.raise_for_status()

                    content_type = r.headers.get("content-type", "")
                    if "json" not in content_type.lower():
                        raise ValueError(
                            f"Expected JSON from {url}, got {content_type!r}. "
                            f"EMA may have moved the file — check "
                            f"docs/data-sources.md for the current URL."
                        )

                    data = r.json()

                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict):
                        for key in ("data", "results", "items", "medicines", "documents"):
                            if key in data and isinstance(data[key], list):
                                return data[key]
                        for v in data.values():
                            if isinstance(v, list):
                                return v
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

    async def persist(self, records: list[dict]) -> int:
        from app.database import SessionLocal

        # Cap hard — 73K records/day is too much
        capped = records[:500]

        async with SessionLocal() as session:
            for rec in capped:
                ext_id = str(
                    rec.get("id")
                    or rec.get("ema_id")
                    or rec.get("medicine_id")
                    or ""
                )[:255]
                await session.execute(text("""
                    INSERT INTO change_events
                        (source, entity_type, external_id, change_type,
                         changed_fields, raw_payload)
                    VALUES ('EMA', 'medicine', :eid, 'added',
                            '{}'::jsonb, :payload)
                """), {
                    "eid": ext_id,
                    "payload": json.dumps(rec, default=str),
                })
            await session.commit()
        return len(capped)