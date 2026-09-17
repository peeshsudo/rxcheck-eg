-- ============================================================
-- RxCheck EG — Core Schema
-- ============================================================

-- Canonical drug concepts (anchored to RxNorm RXCUI where possible)
CREATE TABLE drugs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rxcui           VARCHAR(20) UNIQUE,         -- RxNorm anchor
    generic_en      VARCHAR(255) NOT NULL,
    generic_ar      VARCHAR(255),
    drug_class      VARCHAR(255),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_drugs_generic_en_trgm ON drugs USING gin (generic_en gin_trgm_ops);
CREATE INDEX idx_drugs_generic_ar_trgm ON drugs USING gin (generic_ar gin_trgm_ops);

-- Marketed products (one row per brand per market)
CREATE TABLE products (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    drug_id         UUID NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    brand_en        VARCHAR(255),
    brand_ar        VARCHAR(255),
    market          VARCHAR(10) NOT NULL,       -- 'EG', 'US', 'EU'
    registration_no VARCHAR(100),               -- EDA reg number, NDC, EMA number
    manufacturer    VARCHAR(255),
    form            VARCHAR(100),               -- tablet, syrup, injection
    strength        VARCHAR(100),
    status          VARCHAR(20) DEFAULT 'active',
    source          VARCHAR(20) NOT NULL,       -- 'EDA', 'FDA', 'EMA', 'manual'
    source_url      TEXT,
    last_synced_at  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(market, registration_no)
);

CREATE INDEX idx_products_drug_id ON products(drug_id);
CREATE INDEX idx_products_market ON products(market);
CREATE INDEX idx_products_brand_trgm ON products USING gin (brand_en gin_trgm_ops);

-- Interaction records (pairwise, versioned)
CREATE TABLE interactions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    drug_a_id       UUID NOT NULL REFERENCES drugs(id),
    drug_b_id       UUID NOT NULL REFERENCES drugs(id),
    severity        VARCHAR(20) NOT NULL CHECK (severity IN ('severe','moderate','mild','unknown')),
    effect_en       TEXT NOT NULL,
    effect_ar       TEXT,
    management_en   TEXT,
    management_ar   TEXT,
    source          VARCHAR(50) NOT NULL,       -- 'FDA', 'EMA', 'EDA', 'textbook'
    source_citation TEXT,
    reviewer_name   VARCHAR(255),
    reviewer_approved_at TIMESTAMPTZ,
    version         INTEGER DEFAULT 1,
    is_current      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT no_self_interaction CHECK (drug_a_id <> drug_b_id),
    CONSTRAINT ordered_pair CHECK (drug_a_id < drug_b_id)
);

CREATE INDEX idx_interactions_pair ON interactions(drug_a_id, drug_b_id) WHERE is_current;
CREATE INDEX idx_interactions_severity ON interactions(severity);

-- Curation proposals (maker-checker workflow)
CREATE TABLE proposals (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type            VARCHAR(20) NOT NULL,       -- 'add', 'update', 'delete'
    payload         JSONB NOT NULL,
    summary         TEXT NOT NULL,
    proposed_by     VARCHAR(255) NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    decided_by      VARCHAR(255),
    decided_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Immutable audit log
CREATE TABLE audit_log (
    id              BIGSERIAL PRIMARY KEY,
    ts              TIMESTAMPTZ DEFAULT NOW(),
    actor           VARCHAR(255) NOT NULL,
    action          VARCHAR(100) NOT NULL,
    entity_type     VARCHAR(50),
    entity_id       UUID,
    detail          JSONB,
    prev_hash       VARCHAR(64),
    hash            VARCHAR(64) NOT NULL
);

CREATE INDEX idx_audit_ts ON audit_log(ts DESC);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);

-- Source sync state
CREATE TABLE sync_state (
    source          VARCHAR(20) PRIMARY KEY,
    last_run_at     TIMESTAMPTZ,
    last_success_at TIMESTAMPTZ,
    records_synced  INTEGER DEFAULT 0,
    last_error      TEXT
);

-- Change events (what we detected this run — feeds review queue)
CREATE TABLE change_events (
    id              BIGSERIAL PRIMARY KEY,
    source          VARCHAR(20) NOT NULL,
    entity_type     VARCHAR(50) NOT NULL,
    external_id     VARCHAR(255),
    change_type     VARCHAR(20) NOT NULL,       -- added, updated, removed
    changed_fields  JSONB,
    raw_payload     JSONB,
    detected_at     TIMESTAMPTZ DEFAULT NOW(),
    processed       BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_change_events_unprocessed ON change_events(processed) WHERE NOT processed;

-- User medication schedules (patient-facing)
CREATE TABLE schedules (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL,
    product_id      UUID REFERENCES products(id),
    custom_name     VARCHAR(255),
    time_slots      JSONB NOT NULL,             -- ["fajr","maghrib"]
    food_relation   VARCHAR(20),                -- empty, before, with, after
    dose_note       TEXT,
    active          BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_schedules_user ON schedules(user_id) WHERE active;