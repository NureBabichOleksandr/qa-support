from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Імена обмежень як у sql/01_restore_QA_Support.sql: pk_<table>, uq_<table>_<col>, fk_...
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Базовий клас ORM-моделей.

    Схема БД QA_Support змінюється лише міграціями Alembic (alembic/versions).
    Моделі відтворюють схему ЛР1–ЛР2 один в один: INT IDENTITY ключі, DATETIME2,
    назви таблиць і обмежень як у звітах.

    Важливо для SQL Server: якщо на таблиці є тригер (тригери ЛР2), INSERT/UPDATE
    з OUTPUT inserted падає. Для таких моделей вимикай RETURNING:
        __table_args__ = {"implicit_returning": False}
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
