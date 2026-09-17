CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";   -- for fuzzy drug name matching
CREATE EXTENSION IF NOT EXISTS "vector";    -- pgvector for RAG embeddings