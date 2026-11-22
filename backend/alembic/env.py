import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.database import ENGINE_OPTIONS
from app.core.models import Base

# Моделі кожного модуля: без імпорту autogenerate не побачить таблицю
from app.modules.evaluations.models import (  # noqa: F401
    QaEvaluation,
    QaEvaluationCopy,
    QaEvaluationPromptBlock,
)
from app.modules.prompt_blocks.models import PromptBlock  # noqa: F401
from app.modules.tickets.models import TicketSlaCache  # noqa: F401
from app.modules.topics.models import CanonicalTopic  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


# Alembic викликає ці функції синхронно (run_sync) — виняток з async-правила.
def run_migrations_offline() -> None:
    """`alembic upgrade head --sql` — генерує SQL-скрипт (з GO) без підключення до БД."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named", **ENGINE_OPTIONS},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool, **ENGINE_OPTIONS)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
