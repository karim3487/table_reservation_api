import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    ENV: str = 'dev'
    DEBUG: bool = False
    APP_NAME: str = "Table Reservation API"
    API_VERSION: str

    # PostgreSQL
    DB_NAME: str = "table_reservation"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_SUFFIX: str = ""

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}{self.DB_SUFFIX}"
        )

    class Config:
        env = os.getenv("ENV", "dev")
        env_file = f".env.{env}" if env != "dev" else ".env"
