from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import Settings

settings = Settings()

engine = create_engine(settings.db_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    return SessionLocal
