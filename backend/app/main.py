import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError

from app.core.config import settings
from app.core.database import engine
from app.core.db_errors import SqlServerError
from app.core.exceptions import AppException
from app.modules.router import api_router

logger = logging.getLogger(f"{settings.APP_NAME}.main")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # тут створюються спільні async-ресурси (httpx.AsyncClient тощо) і кладуться в app.state
    yield
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, **exc.extra})


@app.exception_handler(DBAPIError)
async def database_exception_handler(_: Request, exc: DBAPIError) -> JSONResponse:
    error = SqlServerError(exc)
    if error.is_user_error:
        return JSONResponse(
            status_code=400,
            content={"detail": error.message, "source": "database", "error_number": error.number},
        )
    logger.error("Unhandled database error %s", error.number)
    return JSONResponse(status_code=500, content={"detail": "Database error"})


app.include_router(api_router)
