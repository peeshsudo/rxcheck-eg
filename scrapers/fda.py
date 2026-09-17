"""FDA openFDA sync — pulls drug labels and extracts interaction sections."""
import httpx
from scrapers.base import BaseScraper


class FDAScraper(BaseScraper):
    source = "FDA"
    BASE = "https://api.fda.gov/drug/label.json"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def fetch_all(self) -> list[dict]:
        params = {"limit": 100}
        if self.api_key:
            params["api_key"] = self.api_key

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(self.BASE, params=params)
            r.raise_for_status()
            return r.json().get("results", [])

    async def fetch_interactions(self, generic_name: str) -> list[str]:
        """Fetch only the drug_interactions section for one drug."""
        params = {"search": f"openfda.generic_name:{generic_name}", "limit": 1}
        if self.api_key:
            params["api_key"] = self.api_key
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(self.BASE, params=params)
            if r.status_code != 200:
                return []
            results = r.json().get("results", [])
            if not results:
                return []
            return results[0].get("drug_interactions", [])