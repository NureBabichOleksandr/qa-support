from collections.abc import Sequence
from typing import Any

from sqlalchemy import Connection, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories import BaseRepository
from app.modules.topics.models import CanonicalTopic

# FUNCTION
TOP_TOPIC_BY_AGENT_NAME = text("SELECT topic_label FROM dbo.TOP_TOPIC_BY_AGENT_NAME(:agent_name)")

# PROCEDURES
SET_TOPIC_PRIORITY = text(
    "EXEC dbo.SET_TOPIC_PRIORITY @topic_label = :topic_label, @priority_percent = :priority_percent"
)

SET_TOP_ORGANIZATION_FOR_TOPIC = """
SET NOCOUNT ON;
DECLARE @rc INT;
EXEC @rc = dbo.SET_TOP_ORGANIZATION_FOR_TOPIC @topic_label = ?;
SET NOCOUNT OFF;
SELECT @rc AS rc;
"""

MAX_RESULT_SETS = 20


def _fetch_return_code(sync_conn: Connection, sql: str, params: tuple[Any, ...]) -> int:
    dbapi_connection = sync_conn.connection.dbapi_connection
    if dbapi_connection is None:
        raise RuntimeError("DBAPI connection is not available")
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute(sql, params)
        for _ in range(MAX_RESULT_SETS):
            if cursor.description is not None:
                row = cursor.fetchone()
                if row is None:
                    break
                return int(row[0])
            cursor.nextset()
        raise RuntimeError("Процедура не повернула код повернення")
    finally:
        cursor.close()


class TopicRepository(BaseRepository[CanonicalTopic]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CanonicalTopic, session)

    async def list_filtered(
        self, *, search: str | None, is_active: bool | None, skip: int, limit: int
    ) -> tuple[Sequence[CanonicalTopic], int]:
        stmt = select(CanonicalTopic).order_by(CanonicalTopic.canonical_topic_id)
        if search:
            stmt = stmt.where(CanonicalTopic.topic_label.contains(search.strip()))
        if is_active is not None:
            stmt = stmt.where(CanonicalTopic.is_active.is_(is_active))
        return await self.paginate(stmt, skip=skip, limit=limit)

    async def get_by_label(self, topic_label: str) -> CanonicalTopic | None:
        stmt = (
            select(CanonicalTopic)
            .where(CanonicalTopic.topic_label == topic_label)
            .order_by(CanonicalTopic.canonical_topic_id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def top_topics_by_agent(self, agent_name: str) -> Sequence[str]:
        result = await self.session.execute(TOP_TOPIC_BY_AGENT_NAME, {"agent_name": agent_name})
        return result.scalars().all()

    async def set_priority(self, topic_label: str, priority_percent: int) -> None:
        await self.session.execute(
            SET_TOPIC_PRIORITY,
            {"topic_label": topic_label, "priority_percent": priority_percent},
        )

    async def set_top_organization(self, topic_label: str) -> int:
        connection = await self.session.connection()
        return await connection.run_sync(
            _fetch_return_code, SET_TOP_ORGANIZATION_FOR_TOPIC, (topic_label,)
        )
