from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from app.core.models import Base


class BaseRepository[ModelType: Base]:
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: Any) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        # SQL Server вимагає ORDER BY для OFFSET/FETCH
        stmt = (
            select(self.model)
            .order_by(*self.model.__mapper__.primary_key)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def paginate(
        self,
        stmt: Select[ModelType],
        *,
        skip: int,
        limit: int,
        options: Sequence[ORMOption] = (),
    ) -> tuple[Sequence[ModelType], int]:
        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
        total = (await self.session.execute(count_stmt)).scalar_one()
        result = await self.session.execute(stmt.options(*options).offset(skip).limit(limit))
        return result.scalars().unique().all(), total

    async def create(self, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(
        self, db_obj: ModelType, *, exclude_none: bool = True, **kwargs: Any
    ) -> ModelType:
        for key, value in kwargs.items():
            if hasattr(db_obj, key) and not (exclude_none and value is None):
                setattr(db_obj, key, value)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()
