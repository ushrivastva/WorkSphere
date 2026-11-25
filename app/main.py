from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.api.dependencies import DatabaseSession
from app.api.router import api_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/db-check")
def database_check(db: DatabaseSession):
    result = db.execute(text("SELECT 1")).scalar_one()

    return {
        "database": "connected",
        "result": result
    }

