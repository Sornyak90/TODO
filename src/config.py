from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    # Auth
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
