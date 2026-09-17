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

    @abstractmethod
    async def detect_changes(self, previous: dict, current: dict