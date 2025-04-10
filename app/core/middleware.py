import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import Settings

logger = logging.getLogger("app.middleware.request")

settings = Settings()


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            "%s:%s | %s %s | %d | %.2f sec",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    allowed_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
    if settings.ENV == "test":
        allowed_hosts = ["*"]

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )
