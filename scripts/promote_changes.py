import sys
sys.path.insert(0, "/app")

"""
Promote change_events → drugs/products.

Run:
    docker-compose exec scheduler python /app/scripts/promote_changes.py
"""
import sys
sys.path.insert(0, "/app")

import asyncio
import json
import logging
from sqlalchemy import text
from app.database import SessionLocal
import asyncio
import json
import logging

from sqlalchemy import text
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("promoter")


def _first(val):
    if isinstance(val, list):
        return val[0] if val else None
    return val


def extract_fda(rec: dict) -> dict | None:
    """Normalize an openFDA drug label."""
    openfda = rec.get("openfda", {}) or {}
    generic = _first(openfda.get("generic_name"))
    brand = _first(openfda.get("brand_name"))
    if not generic and not brand:
        return None
    return {
        "generic_en": (generic or brand).strip().title(),
        "brand_en": (brand or "").strip().title() or None,
        "manufacturer": _first(openfda.get("manufacturer_name")),
        "registration_no": _first(openfda.get("product_ndc")),
        "atc_code": None,
        "drug_class": None,
        "market": "US",
        "source": "FDA",
        "source_url": None,
    }


def extract_ema(rec: dict) -> dict | None:
    """Normalize an EMA medicine record (real field names, verified)."""
    brand = (rec.get("name_of_medicine") or "").strip()
    generic = (
        rec.get("international_non_proprietary_name_common_name")
        or rec.get("active_substance")
        or ""
    ).strip()
    if not generic and not brand:
        return None
    return {
        "generic_en": (generic or brand).title(),
        "brand_en": brand or None,
        "manufacturer": rec.get(
            "marketing_authorisation_developer_applicant_holder"
        ),
        "registration_no": rec.get("ema_product_number"),
        "atc_code": rec.get("atc_code_human") or None,
        "drug_class": rec.get("therapeutic_area_mesh") or None,
        "market": "EU",
        "source": "EMA",
        "source_url": rec.get("medicine_url"),
    }


EXTRACTORS = {"FDA": extract_fda, "EMA": extract_ema}


async def _upsert_drug(session, item: dict) -> tuple[str | None, bool]:
    """Return (drug_id, created)."""
    # Lookup first — safer than ON CONFLICT against a functional index
    row = (await session.execute(
        text("SELECT id FROM drugs WHERE lower(generic_en) = lower(:g) LIMIT 1"),
        {"g": item["generic_en"]},
    )).first()
    if row:
        return str(row[0]), False

    row = (await session.execute(
        text("""
            INSERT INTO drugs (generic_en, drug_class)
            VALUES (:g, :c)
            RETURNING id
        """),
        {"g": item["generic_en"], "c": item.get("drug_class")},
    )).first()
    return (str(row[0]), True) if row else (None, False)


async def _upsert_product(session, drug_id: str, item: dict) -> bool:
    """Return True if a new product row was created."""
    if not item.get("brand_en"):
        return False
    row = (await session.execute(
        text("""
            SELECT id FROM products
            WHERE drug_id = :d
              AND lower(coalesce(brand_en, '')) = lower(:b)
              AND market = :m
            LIMIT 1
        """),
        {"d": drug_id, "b": item["brand_en"], "m": item["market"]},
    )).first()
    if row:
        return False

    await session.execute(
        text("""
            INSERT INTO products
                (drug_id, brand_en, market, manufacturer,
                 registration_no, source, source_url)
            VALUES (:d, :b, :m, :mf, :r, :s, :u)
        """),
        {
            "d": drug_id,
            "b": item["brand_en"],
            "m": item["market"],
            "mf": item.get("manufacturer"),
            "r": item.get("registration_no"),
            "s": item["source"],
            "u": item.get("source_url"),
        },
    )
    return True


async def promote_batch(session, source: str, extractor, limit: int = 200) -> dict:
    rows = (await session.execute(
        text("""
            SELECT id, raw_payload FROM change_events
            WHERE source = :s AND NOT processed
            ORDER BY id
            LIMIT :lim
        """),
        {"s": source, "lim": limit},
    )).all()

    created_drugs = 0
    created_products = 0
    skipped = 0
    processed_ids = []

    for event_id, raw in rows:
        try:
            payload = raw if isinstance(raw, dict) else json.loads(raw)
        except Exception:
            skipped += 1
            processed_ids.append(event_id)
            continue

        item = extractor(payload)
        if not item or not item.get("generic_en"):
            skipped += 1
            processed_ids.append(event_id)
            continue

        drug_id, drug_created = await _upsert_drug(session, item)
        if drug_id:
            created_drugs += int(drug_created)
            if await _upsert_product(session, drug_id, item):
                created_products += 1

        processed_ids.append(event_id)

    if processed_ids:
        await session.execute(
            text("UPDATE change_events SET processed = true WHERE id = ANY(:ids)"),
            {"ids": processed_ids},
        )
    await session.commit()

    return {
        "source": source,
        "batch": len(rows),
        "drugs_created": created_drugs,
        "products_created": created_products,
        "skipped": skipped,
    }


async def main():
    totals = {"drugs": 0, "products": 0, "skipped": 0}
    async with SessionLocal() as session:
        for source, extractor in EXTRACTORS.items():
            log.info("=== Source: %s ===", source)
            for _ in range(50):  # safety cap: 50 batches × 200 = 10k rows/source
                stats = await promote_batch(session, source, extractor)
                log.info("Batch: %s", stats)
                totals["drugs"] += stats["drugs_created"]
                totals["products"] += stats["products_created"]
                totals["skipped"] += stats["skipped"]
                if stats["batch"] < 200:
                    break
    log.info("DONE. Totals: %s", totals)


if __name__ == "__main__":
    asyncio.run(main())