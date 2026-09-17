"""Run with: python -m app.seed"""
import asyncio
from app.database import SessionLocal
from app.models import Drug, Product, Interaction

SEED_DRUGS = [
    {"rxcui": "32968", "generic_en": "clopidogrel", "generic_ar": "كلوبيدوجريل", "drug_class": "Antiplatelet"},
    {"rxcui": "7646",  "generic_en": "omeprazole",  "generic_ar": "أوميبرازول",  "drug_class": "PPI"},
    {"rxcui": "11289", "generic_en": "warfarin",    "generic_ar": "وارفارين",    "drug_class": "Anticoagulant"},
    {"rxcui": "1191",  "generic_en": "aspirin",     "generic_ar": "أسبرين",      "drug_class": "NSAID"},
]


async def main():
    async with SessionLocal() as db:
        for d in SEED_DRUGS:
            db.add(Drug(**d))
        await db.commit()
        print(f"Seeded {len(SEED_DRUGS)} drugs.")


if __name__ == "__main__":
    asyncio.run(main())