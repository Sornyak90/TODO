from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    fake_users: Dict[str, Dict[str, str]] = Field(default_factory=dict)

settings = Settings()
