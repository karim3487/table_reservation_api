from fastapi import FastAPI
from app.errors.base import BaseAppException
from app.errors.handlers import app_exception_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(BaseAppException, app_exception_handler)
