from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    USERS_DB_NAME: str
    USERS_DATABASE_URL: str
    AUTH_VERIFY_URL: str = "http://auth-service:8000/api/v1/auth/verify"


settings = Settings()
