# Architecture

## Data flow
FDA/EMA/EDA → scrapers → change_events → review queue → interactions table
↓
Patient camera → OCR → fuzzy match → drug_id ──→ /interactions/check
↓
severity + bilingual management


## Key decisions

| Decision | Rationale |
|----------|-----------|
| RxNorm RXCUI as anchor | Free, no key, globally unique |
| Pairwise interaction records | Simpler than N-way, matches clinical reality |
| Append-only audit log | Regulatory requirement in regulated markets |
| Arabic-first UI | 90%+ of target users |
| On-device OCR | Works offline, no data leaves phone |
