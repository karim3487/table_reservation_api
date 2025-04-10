from fastapi import Depends

from app.errors import exceptions
from app.models import Table
from app.repositories.table_repository import TableRepository
from app.schemas import TableCreate


class TableService:
    repository: TableRepository

    def __init__(self, repository: TableRepository = Depends()) -> None:
        self.repository = repository

    def create(self, table: TableCreate) -> Table:
        exists = self.repository.get_by_name(table.name)
        if exists:
            raise exceptions.DuplicateTableName(table.name)

        return self.repository.create(Table(**table.model_dump()))

    def delete(self, table_id: int) -> None:
        table = self.repository.get(table_id)
        if not table:
            raise exceptions.TableNotFound(table_id)
        return self.repository.delete(table_id)

    def get(self, table_id: int) -> Table:
        table = self.repository.get(table_id)
        if not table:
            raise exceptions.TableNotFound(table_id)
        return self.repository.get(table_id)

    def get_by_name(self, table_name: str) -> Table:
        return self.repository.get_by_name(table_name)

    def list(
        self, page_size: int | None = 10, start_index: int | None = 0
    ) -> list[Table]:
        return self.repository.list(page_size, start_index)

    def update(self, table_id: int, table_update: TableCreate) -> Table:
        table = self.repository.get(table_id)
        if not table:
            raise exceptions.TableNotFound(table_id)

        other = self.repository.get_by_name(table_update.name)
        if other and other.id != table_id:
            raise exceptions.TableUpdateConflict(table_update.name)

        updated_table = Table(id=table_id, **table_update.model_dump())
        return self.repository.update(updated_table)
