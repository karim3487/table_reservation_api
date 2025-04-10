from sqlalchemy.orm import Session

from fastapi import Depends
from app.db import get_db_session
from app.models import Table


class TableRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_session)) -> None:
        self.db = db

    def list(self, limit: int | None, start: int | None) -> list[Table]:
        query = self.db.query(Table)
        return query.offset(start).limit(limit).all()

    def get(self, table_id: int) -> Table | None:
        return self.db.get(Table, table_id)

    def get_by_name(self, name: str) -> Table | None:
        return self.db.query(Table).filter_by(name=name).first()

    def create(self, table: Table) -> Table:
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def update(self, table: Table) -> Table:
        self.db.merge(table)
        self.db.commit()
        return table

    def delete(self, table_id: int) -> None:
        self.db.query(Table).filter(Table.id == table_id).delete()
        self.db.commit()
