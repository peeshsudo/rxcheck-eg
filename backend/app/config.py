"""
Configuration loader with fail-fast validation.

Changes from prior version:
- Refuses to start if CHANGE_ME placeholders remain
- Split EMA_BASE_URL into two real JSON endpoints
- Enforces DEBUG=false when ENVIRONMENT=production
- Added ADMIN_KEY for admin endpoint auth
"""
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PLACEHOLDER_PREFIX = "CHANGE_ME"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ==== Environment ====
    environment: str = Field(default="development")
    debug: bool = Field(default=True)

    # ==== Database ====
    database_url: str

    # ==== Backend ====
    backend_port: int = 8000
    backend_secret_key: str
    backend_admin_key: str
    backend_cors_origins: str = "http://localhost:3000"

    # ==== External APIs ====
    openfda_api_key: str | None = None
    rxnav_base_url: str = "https://rxnav.nlm.nih.gov/REST"
    ema_medicines_json_url: str = "https://www.ema.europa.eu/en/media/67423"
    ema_documents_json_url: str = "https://www.ema.europa.eu/en/media/67425"
    eda_portal_url: str = (
        "https://eservices.edaegypt.gov.eg/EDASearch/SearchRegDrugs.aspx"
    )

    # ==== AI Agent ====
    openai_api_key: str | None = None
    agent_model: str = "gpt-4o-mini"
    vector_db_url: str = "http://chromadb:8000"

    # ==== Derived ====
    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    # ==== Validators ====
    @field_validator("database_url", "backend_secret_key", "backend_admin_key")
    @classmethod
    def reject_placeholders(cls, v: str, info) -> str:
        if PLACEHOLDER_PREFIX in v:
            raise ValueError(
                f"{info.field_name} still contains '{PLACEHOLDER_PREFIX}'. "
                f"Edit your .env file and replace every placeholder before starting."
            )
        return v

    @field_validator("backend_secret_key")
    @classmethod
    def secret_key_min_length(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("BACKEND_SECRET_KEY must be at least 32 characters.")
        return v

    @model_validator(mode="after")
    def enforce_production_rules(self) -> "Settings":
        if self.is_production and self.debug:
            raise ValueError(
                "DEBUG must be false when ENVIRONMENT=production."
            )
        return self


settings = Settings()