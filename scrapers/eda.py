"""EDA (Egyptian Drug Authority) sync — placeholder until API access is granted.

The EDA portal at eservices.edaegypt.gov.eg does not currently expose a
public API. Options:
  1. Request official API access from EDA (in progress)
  2. Use the public search UI with careful rate-limiting (ToS risk)
  3. Manual CSV imports maintained by a data operator

Until access is granted, this scraper returns an empty list. EDA-sourced
drug data comes from database/init/03_seed.sql (manual curation).
"""

import logging
from typing import Any, Dict, List

import httpx

from scrapers.base import BaseScraper

logger = logging.getLogger("rxcheck.eda_scraper")


class EDAClientException(Exception):
    """Custom exception for EDA API communication errors."""


class EDAPrivateClient:
    """Client for querying EDA registries and product catalogs.

    Currently returns mock data because the live API is not public.
    Replace `_local_eda_fallback` with real HTTP calls once access is granted.
    """

    def __init__(
        self,
        base_url: str = "https://www.edaegypt.gov.eg/api",
        timeout: float = 10.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def search_drug_by_trade_name(
        self, trade_name: str
    ) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/v1/products/search"
        params = {"query": trade_name, "market": "EG"}
        logger.info("Executing EDA API lookup for query: %s", trade_name)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    return response.json().get("results", [])
                if response.status_code == 404:
                    return []
                raise EDAClientException(
                    f"EDA service error: HTTP {response.status_code}"
                )
        except httpx.RequestError as exc:
            logger.warning(
                "EDA connection failed (%s). Using local fallback.", exc
            )
            return self._local_eda_fallback(trade_name)

    def _local_eda_fallback(self, trade_name: str) -> List[Dict[str, Any]]:
        mock_registry = [
            {
                "eda_reg_no": "EG-EDA-2024-5891",
                "trade_name": "Cidophage 500mg",
                "generic_name": "Metformin HCl",
                "active_ingredients": ["Metformin"],
                "manufacturer": "Chemical Industries Development (CID) - Egypt",
            },
            {
                "eda_reg_no": "EG-EDA-2023-1102",
                "trade_name": "Marevan 5mg",
                "generic_name": "Warfarin Sodium",
                "active_ingredients": ["Warfarin"],
                "manufacturer": "Kahira Pharmaceuticals - Egypt",
            },
            {
                "eda_reg_no": "EG-EDA-2022-9920",
                "trade_name": "Ciprofar 500mg",
                "generic_name": "Ciprofloxacin",
                "active_ingredients": ["Ciprofloxacin"],
                "manufacturer": "Pharco Pharmaceuticals - Egypt",
            },
        ]
        return [
            item
            for item in mock_registry
            if trade_name.lower() in item["trade_name"].lower()
        ]


class EDAScraper(BaseScraper):
    """Sync adapter. Returns [] until EDA opens a public API."""

    source = "EDA"

    async def fetch_all(self) -> list[dict]:
        print("[EDA] No public API — skipping (see scrapers/eda.py docstring)")
        return []

    async def persist(self, records: list[dict]) -> int:
        return 0