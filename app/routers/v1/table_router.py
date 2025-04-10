from fastapi import APIRouter, Depends, status

from app.schemas import TableRead, TableCreate
from app.services.table_service import TableService

TableRouter = APIRouter(prefix="/v1/tables", tags=["tables"])


@TableRouter.get("/", response_model=list[TableRead])
def index(
    page_size: int | None = 100,
    start_index: int | None = 0,
    table_service: TableService = Depends(),
):
    return [table for table in table_service.list(page_size, start_index)]


@TableRouter.get("/{id}", response_model=TableRead)
def get(table_id: int, table_service: TableService = Depends()):
    return table_service.get(table_id)


@TableRouter.post(
    "/",
    response_model=TableRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    table: TableCreate,
    table_service: TableService = Depends(),
):
    return table_service.create(table)


@TableRouter.patch("/{id}", response_model=TableRead)
def update(
    table_id: int,
    author: TableCreate,
    table_service: TableService = Depends(),
):
    return table_service.update(table_id, author)


@TableRouter.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(table_id: int, table_service: TableService = Depends()):
    return table_service.delete(table_id)
