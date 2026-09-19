'''from abc import ABC, abstractmethod
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

    @abstractmethod
    async def detect_changes(
        self, previous: dict, current: dict
    ) -> list[ChangeEvent]:
        """Compare two snapshots and return the list of changes."""
        ...
'''
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
        """Full sync cycle. Default: fetch and return."""
        return await self.fetch_all()
        
    # NOT abstract — provides a working default
    async def detect_changes(
        self, previous: dict, current: dict
    ) -> list[ChangeEvent]:
        """Default: diff records by external_id."""
        events: list[ChangeEvent] = []
        prev_items = {r["external_id"]: r for r in previous.get("items", [])}
        curr_items = {r["external_id"]: r for r in current.get("items", [])}
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