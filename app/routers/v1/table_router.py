import logging

from fastapi import APIRouter, Depends, status

from app.schemas import TableCreate, TableRead
from app.services.table_service import TableService

logger = logging.getLogger("app.routers.tables")

TableRouter = APIRouter(prefix="/v1/tables", tags=["tables"])


@TableRouter.get("/", response_model=list[TableRead])
def index(
    page_size: int | None = 100,
    start_index: int | None = 0,
    table_service: TableService = Depends(),
):
    return [table for table in table_service.list(page_size, start_index)]


@TableRouter.get("/{table_id}", response_model=TableRead)
def get(table_id: int, table_service: TableService = Depends()):
    logger.info("Fetching table with id=%s", table_id)
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
    logger.info("Creating new table: %s", table.name)
    return table_service.create(table)


@TableRouter.patch("/{table_id}", response_model=TableRead)
def update(
    table_id: int,
    table: TableCreate,
    table_service: TableService = Depends(),
):
    logger.info("Updating table id=%s", table_id)
    return table_service.update(table_id, table)


@TableRouter.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(table_id: int, table_service: TableService = Depends()):
    logger.info("Deleting table with id=%s", table_id)
    return table_service.delete(table_id)
