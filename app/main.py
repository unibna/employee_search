from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.api.router import api_router


app = FastAPI(
    title="Employee Search API",
    description="Backend API for employee search",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(api_router, prefix=settings.api_v1_prefix)

