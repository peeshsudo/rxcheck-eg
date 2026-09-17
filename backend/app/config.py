from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    backend_secret_key: str
    backend_cors_origins: str = "http://localhost:3000"

    openfda_api_key: str | None = None
    rxnav_base_url: str = "https://rxnav.nlm.nih.gov/REST"
    ema_base_url: str = "https://www.ema.europa.eu/en/medicines"
    eda_base_url: str = "https://eservices.edaegypt.gov.eg"

    openai_api_key: str | None = None
    agent_model: str = "gpt-4o-mini"
    vector_db_url: str = "http://chromadb:8000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",")]


settings = Settings()