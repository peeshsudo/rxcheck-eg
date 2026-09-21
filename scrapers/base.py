from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ChangeEvent:
    source: str
    entity_type: str
    external_id: str
    change_type: str  # added | updated | removed
    changed_fields: dict
    raw_payload: dict


class BaseScraper(ABC):
    source: str

    @abstractmethod
    async def fetch_all(self) -> list[dict]:
        """Pull the full current dataset from the upstream source."""
        ...

    async def run(self) -> list[dict]:
        """Full sync cycle: fetch → persist → update sync_state."""
        records = await self.fetch_all()
        try:
            count = await self.persist(records)
            await self.update_sync_state(success=True, count=count, error=None)
            return records
        except Exception as e:
            await self.update_sync_state(success=False, count=0, error=str(e))
            raise

    async def persist(self, records: list[dict]) -> int:
        """Default: no-op. Override per scraper."""
        return len(records)

    async def update_sync_state(
        self, success: bool, count: int, error: str | None = None
    ) -> None:
        """Write to sync_state table."""
        from app.database import SessionLocal
        from sqlalchemy import text

        async with SessionLocal() as session:
            await session.execute(text("""
                INSERT INTO sync_state
                    (source, last_run_at, last_success_at, records_synced, last_error)
                VALUES (
                    :src,
                    NOW(),
                    CASE WHEN :ok THEN NOW() ELSE NULL END,
                    :n,
                    :err
                )
                ON CONFLICT (source) DO UPDATE SET
                    last_run_at = NOW(),
                    last_success_at = CASE
                        WHEN :ok THEN NOW()
                        ELSE sync_state.last_success_at
                    END,
                    records_synced = :n,
                    last_error = :err
            """), {
                "src": self.source,
                "ok": success,
                "n": count,
                "err": error,
            })
            await session.commit()

    async def detect_changes(
        self, previous: dict, current: dict
    ) -> list[ChangeEvent]:
        """Default: diff records by external_id."""
        events: list[ChangeEvent] = []
        prev_items = {r.get("external_id"): r for r in previous.get("items", [])}
        curr_items = {r.get("external_id"): r for r in current.get("items", [])}
        etype = current.get("entity_type", previous.get("entity_type", "unknown"))

        for ext_id, curr in curr_items.items():
            if ext_id not in prev_items:
                events.append(ChangeEvent(
                    source=self.source, entity_type=etype,
                    external_id=ext_id, change_type="added",
                    changed_fields={}, raw_payload=curr,
                ))
            elif prev_items[ext_id] != curr:
                changed = {
                    k: curr[k] for k in curr
                    if prev_items[ext_id].get(k) != curr[k]
                }
                events.append(ChangeEvent(
                    source=self.source, entity_type=etype,
                    external_id=ext_id, change_type="updated",
                    changed_fields=changed, raw_payload=curr,
                ))

        for ext_id in prev_items.keys() - curr_items.keys():
            events.append(ChangeEvent(
                source=self.source, entity_type=etype,
                external_id=ext_id, change_type="removed",
                changed_fields={}, raw_payload=prev_items[ext_id],
            ))

        return events