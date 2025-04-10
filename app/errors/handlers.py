from fastapi import Request
from fastapi.responses import JSONResponse
from app.errors.base import BaseAppException


async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
