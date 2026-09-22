from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal["local", "test", "staging", "production"]


class Settings(BaseSettings):
    app_name: str = "DevPilot AI"
    app_version: str = "0.1.0"
    environment: Environment = "local"

    api_v1_prefix: str = "/api/v1"

    log_level: str = "INFO"

    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    embedding_provider: str = "mock"
    embedding_dimension: int = 384
    embedding_model: str = "mock-lexical-v1"

    document_repository: Literal["memory", "database"] = "memory"
    rag_default_top_k: int = 4
    rag_max_top_k: int = 10
    rag_min_similarity: float = 0.0

    jwt_secret_key: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    rate_limit_enabled: bool = True
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    database_url: str = Field(
        default="sqlite:///./devpilot.db",
        description="Primary application database URL",
    )

    redis_url: str = "redis://localhost:6379/0"

    otel_enabled: bool = False
    otel_service_name: str = "devpilot-ai"
    otel_exporter_otlp_endpoint: str = ""
    cors_origins: str = (
        "http://localhost:8080,http://127.0.0.1:8080,"
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
