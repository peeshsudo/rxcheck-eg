# Data Sources

## FDA
- Endpoint: https://api.fda.gov/drug/label.json
- Auth: Optional API key (higher rate limits)
- Refresh: Daily
- Notes: `drug_interactions` field is the primary source

## EMA
- Endpoint: EMA medicines data downloads (JSON)
- Refresh: Twice daily (06:00, 18:00 CET)
- Notes: EU-marketed products only

## EDA (Egypt)
- Portal: https://eservices.edaegypt.gov.eg
- API: Not public — request official access
- Fallback: Manual CSV imports maintained by data operator
- Refresh: Weekly or on EDA announcement

## RxNorm
- Endpoint: https://rxnav.nlm.nih.gov/REST
- Auth: None
- Rate limit: 2 req/s
- Purpose: Normalize names → RXCUI