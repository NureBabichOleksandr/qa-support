"""ЛР1, додатки В–Е: функції та процедури

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-22

Тексти перенесено дослівно з sql/01_restore_QA_Support.sql.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _execute(sql: str) -> None:
    # кожен CREATE FUNCTION/PROCEDURE — окремий batch; двокрапки не є bind-параметрами
    op.execute(sa.text(sql.replace(":", r"\:")))


# Додаток В, завдання 1
TOP_TOPIC_BY_AGENT_NAME = """
CREATE OR ALTER FUNCTION dbo.TOP_TOPIC_BY_AGENT_NAME (@agent_name NVARCHAR(50))
RETURNS @result TABLE (
    topic_label NVARCHAR(100)
)
AS
BEGIN
    INSERT INTO @result (topic_label)
    SELECT ct.topic_label
    FROM ticket_sla_cache AS t
    JOIN qa_evaluation    AS qa ON qa.ticket_id = t.ticket_id
    JOIN canonical_topics AS ct ON ct.canonical_topic_id = qa.canonical_topic_id
    WHERE t.agent_name = @agent_name
    GROUP BY ct.canonical_topic_id, ct.topic_label
    HAVING COUNT(*) = (
        SELECT MAX(topics_count.cnt)
        FROM (
            SELECT COUNT(*) AS cnt
            FROM ticket_sla_cache AS t2
            JOIN qa_evaluation    AS qa2 ON qa2.ticket_id = t2.ticket_id
            WHERE t2.agent_name = @agent_name
            GROUP BY qa2.canonical_topic_id
        ) AS topics_count
    );

    IF NOT EXISTS (SELECT 1 FROM @result)
        INSERT INTO @result VALUES (N'Відсутні оцінки');
    RETURN;
END
"""

# Додаток Г, завдання 10
SET_TOPIC_PRIORITY = """
CREATE OR ALTER PROCEDURE dbo.SET_TOPIC_PRIORITY
    @topic_label      NVARCHAR(100),
    @priority_percent INT
AS
BEGIN
    SET NOCOUNT ON;
    IF @topic_label IS NULL OR LTRIM(RTRIM(@topic_label)) = N''
    BEGIN
        THROW 50001, N'Параметр @topic_label є обов''язковим.', 1;
        RETURN;
    END

    UPDATE canonical_topics
    SET meaning    = N'Пріоритет ' + CAST(@priority_percent AS NVARCHAR(10)) + N' %',
        updated_at = SYSDATETIME()
    WHERE topic_label = @topic_label;

    IF @@ROWCOUNT = 0
        PRINT N'Тему «' + @topic_label + N'» не знайдено';
    ELSE
        PRINT N'Поле meaning теми «' + @topic_label + N'» оновлено';
END
"""

# Додаток Д, завдання 4
MAX_EVALUATION_BY_TOPIC = """
CREATE OR ALTER FUNCTION dbo.MAX_EVALUATION_BY_TOPIC (@topic_label NVARCHAR(100))
RETURNS @result TABLE (
    qa_evaluation_id INT           NULL,
    ticket_id        INT           NULL,
    overall_score    DECIMAL(4,1)  NULL,
    result           NVARCHAR(20)  NULL,
    created_at       DATETIME2     NULL,
    info             NVARCHAR(200) NULL
)
AS
BEGIN
    INSERT INTO @result (qa_evaluation_id, ticket_id, overall_score, result, created_at)
    SELECT qa.qa_evaluation_id, qa.ticket_id, qa.overall_score, qa.result, qa.created_at
    FROM qa_evaluation    AS qa
    JOIN canonical_topics AS ct ON ct.canonical_topic_id = qa.canonical_topic_id
    WHERE ct.topic_label = @topic_label
      AND qa.overall_score = (
          SELECT MAX(qa2.overall_score)
          FROM qa_evaluation    AS qa2
          JOIN canonical_topics AS ct2 ON ct2.canonical_topic_id = qa2.canonical_topic_id
          WHERE ct2.topic_label = @topic_label
      );

    IF NOT EXISTS (SELECT 1 FROM @result)
        INSERT INTO @result (info)
        VALUES (N'Відсутні оцінки теми «' + @topic_label + N'»');
    RETURN;
END
"""

# Додаток Е, завдання 13
SET_TOP_ORGANIZATION_FOR_TOPIC = """
CREATE OR ALTER PROCEDURE dbo.SET_TOP_ORGANIZATION_FOR_TOPIC
    @topic_label NVARCHAR(100)
AS
BEGIN
    DECLARE @org NVARCHAR(100);

    IF NOT EXISTS (SELECT 1 FROM canonical_topics WHERE topic_label = @topic_label)
    BEGIN
        PRINT N'Тему «' + @topic_label + N'» не знайдено';
        RETURN 1;
    END

    SELECT TOP 1 @org = qa.organization_name
    FROM qa_evaluation    AS qa
    JOIN canonical_topics AS ct ON ct.canonical_topic_id = qa.canonical_topic_id
    WHERE ct.topic_label = @topic_label
      AND qa.organization_name IS NOT NULL
    GROUP BY qa.organization_name
    ORDER BY COUNT(DISTINCT qa.ticket_id) DESC;

    IF @org IS NULL
    BEGIN
        PRINT N'Для теми «' + @topic_label + N'» немає оцінок з організацією';
        RETURN 2;
    END

    UPDATE canonical_topics
    SET related_terms = CONVERT(NVARCHAR(10), GETDATE(), 104) + N' ' + @org,
        updated_at    = SYSDATETIME()
    WHERE topic_label = @topic_label;

    PRINT N'Тему «' + @topic_label + N'» оновлено: ' + @org;
    RETURN 0;
END
"""


def upgrade() -> None:
    for sql in (
        TOP_TOPIC_BY_AGENT_NAME,
        SET_TOPIC_PRIORITY,
        MAX_EVALUATION_BY_TOPIC,
        SET_TOP_ORGANIZATION_FOR_TOPIC,
    ):
        _execute(sql)


def downgrade() -> None:
    _execute("DROP PROCEDURE IF EXISTS dbo.SET_TOP_ORGANIZATION_FOR_TOPIC;")
    _execute("DROP FUNCTION IF EXISTS dbo.MAX_EVALUATION_BY_TOPIC;")
    _execute("DROP PROCEDURE IF EXISTS dbo.SET_TOPIC_PRIORITY;")
    _execute("DROP FUNCTION IF EXISTS dbo.TOP_TOPIC_BY_AGENT_NAME;")
