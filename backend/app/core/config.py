from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "qa-support"
    DEBUG: bool = False

    DB_HOST: str = "localhost"
    DB_PORT: int = 1433
    DB_NAME: str = "QA_Support"
    DB_USER: str = "sa"
    DB_PASSWORD: str = ""
    DB_DRIVER: str = "ODBC Driver 18 for SQL Server"
    DB_TRUST_SERVER_CERTIFICATE: bool = True

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL(self) -> URL:
        query = {"driver": self.DB_DRIVER}
        if self.DB_TRUST_SERVER_CERTIFICATE:
            query["TrustServerCertificate"] = "yes"
        return URL.create(
            "mssql+aioodbc",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            query=query,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
