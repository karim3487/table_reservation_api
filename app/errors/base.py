from fastapi import status


class BaseAppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
