from sqlalchemy import Column, Integer, String

from app.db import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=True)
