from fastapi import FastAPI

from app.core.config import Settings
from app.core.logging import setup_logging
from app.core.middleware import register_middleware
from app.errors import register_error_handlers
from app.routers import routers

setup_logging()

settings = Settings()

app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION)


@app.get("/")
def root():
    return {"msg": "Welcome to the Table Reservation API"}


# Add Routers
for router in routers:
    app.include_router(router)

# Exceptions
register_error_handlers(app)

# Middleware
register_middleware(app)
