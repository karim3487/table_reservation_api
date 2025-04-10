from fastapi import status

from app.errors.base import BaseAppException


class TableNotFound(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, table_id: int):
        super().__init__(f"Table with id '{table_id}' not found")


class DuplicateTableName(BaseAppException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, name: str):
        super().__init__(f"Table with name '{name}' already exists")


class TableUpdateConflict(BaseAppException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, name: str):
        super().__init__(f"Cannot update table: name '{name}' is already in use")


class InvalidTableData(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, msg: str = "Invalid table data"):
        super().__init__(msg)


class ReservationNotFound(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Reservation not found"


class ReservationTimeConflict(BaseAppException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, table_id: int):
        super().__init__(f"Table {table_id} is already reserved for this time slot")
