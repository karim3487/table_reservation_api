import logging
import traceback

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors.base import BaseAppException

logger = logging.getLogger("app.exceptions")


async def app_exception_handler(request: Request, exc: BaseAppException):
    logger.warning(
        "AppException | %s %s | %s", request.method, request.url.path, exc.message
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(
        "HTTPException %d | %s %s", exc.status_code, request.method, request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def sanitize_errors(errors: list[dict]) -> list[dict]:
    sanitized = []
    for err in errors:
        err = err.copy()
        if "ctx" in err and "error" in err["ctx"]:
            err["ctx"] = err["ctx"].copy()
            err["ctx"]["error"] = str(err["ctx"]["error"])
        sanitized.append(err)
    return sanitized


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = sanitize_errors(exc.errors())
    logger.warning("ValidationError | %s %s | %s", request.method, request.url.path, errors)
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(
        "UnhandledException | %s %s | %s\n%s",
        request.method,
        request.url.path,
        type(exc).__name__,
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
