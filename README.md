# RxCheck EG

Bilingual (Arabic/English) drug interaction checker for Egyptian patients and pharmacists.

## Quick Start

```bash
cp .env.example .env
make install
make dev



```bash
cp .env.example .env
# Edit .env — set POSTGRES_PASSWORD and BACKEND_SECRET_KEY at minimum
chmod +x scripts/*.sh
./scripts/setup.sh
