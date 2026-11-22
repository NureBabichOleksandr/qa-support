from collections.abc import AsyncGenerator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Спільні опції для всіх engine (застосунок, Alembic, тести).
# deprecate_large_types: UnicodeText/LargeBinary -> NVARCHAR(MAX)/VARBINARY(MAX), а не
# застарілі NTEXT/IMAGE, навіть коли версія сервера невідома (alembic --sql).
ENGINE_OPTIONS: dict[str, Any] = {"deprecate_large_types": True}

engine = create_async_engine(
    settings.DATABASE_URL, pool_pre_ping=True, echo=settings.DEBUG, **ENGINE_OPTIONS
)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]
