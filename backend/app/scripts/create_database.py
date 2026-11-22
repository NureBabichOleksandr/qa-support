"""Створює БД settings.DB_NAME, якщо її ще немає.

Alembic працює всередині цільової БД, тому сама БД створюється окремо:
    python -m app.scripts.create_database && alembic upgrade head
"""

import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

logger = logging.getLogger(f"{settings.APP_NAME}.scripts")

CREATE_IF_MISSING = text(
    """
    IF DB_ID(:name) IS NULL
    BEGIN
        DECLARE @sql NVARCHAR(400) = N'CREATE DATABASE ' + QUOTENAME(:name);
        EXEC (@sql);
        SELECT 1;
    END
    ELSE
        SELECT 0;
    """
)


async def create_database() -> bool:
    engine = create_async_engine(
        settings.DATABASE_URL.set(database="master"), isolation_level="AUTOCOMMIT"
    )
    try:
        async with engine.connect() as conn:
            created = await conn.scalar(CREATE_IF_MISSING, {"name": settings.DB_NAME})
    finally:
        await engine.dispose()
    return bool(created)


def main() -> None:  # точка входу CLI — виняток з async-правила
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    created = asyncio.run(create_database())
    logger.info("Database %s %s", settings.DB_NAME, "created" if created else "already exists")


if __name__ == "__main__":
    main()
