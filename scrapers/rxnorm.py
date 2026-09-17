"""RxNorm normalization — free, no API key."""
import httpx


async def get_rxcui(name: str) -> str | None:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            "https://rxnav.nlm.nih.gov/REST/rxcui.json",
            params={"name": name},
        )
        if r.status_code != 200:
            return None
        ids = r.json().get("idGroup", {}).get("rxnormId", [])
        return ids[0] if ids else None