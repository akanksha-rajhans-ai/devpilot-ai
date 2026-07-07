from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DevPilot AI"
    app_version: str = "0.1.0"
    environment: str = "local"
    llm_provider: str = "mock"

    class Config:
        env_file = ".env"


settings = Settings()
