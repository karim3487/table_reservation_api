from fastapi import FastAPI

app = FastAPI()
from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION
)


@app.get("/")
def root():
    return {"msg": "Welcome to the Table Reservation API"}
