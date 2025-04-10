from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from app.core.config import Settings

settings = Settings()

engine = create_engine(settings.db_url, echo=settings.DEBUG, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
