"""ЛР1, додаток Б: початкові дані

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-22

Дані перенесено дослівно з sql/01_restore_QA_Support.sql. Ця міграція йде ДО тригерів ЛР2
(0004), інакше INSERT у qa_evaluation дописав би номери оцінок у ticket_sla_cache.tags.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _execute(sql: str) -> None:
    # двокрапки в літералах часу ('10:00') інакше сприймаються як bind-параметри
    op.execute(sa.text(sql.replace(":", r"\:")))


CANONICAL_TOPICS = """
INSERT INTO canonical_topics (topic_id, topic_label, meaning) VALUES
(N'TOP-001', N'Біллінг',           N'Питання оплат та рахунків'),
(N'TOP-002', N'Доступ',            N'Проблеми з входом і правами'),
(N'TOP-003', N'Інтеграції',        N'Налаштування сторонніх інтеграцій'),
(N'TOP-004', N'Помилки API',       N'Некоректні відповіді API'),
(N'TOP-005', N'Звіти',             N'Побудова та експорт звітів'),
(N'TOP-006', N'Продуктивність',    N'Повільна робота системи, таймаути'),
(N'TOP-007', N'Відновлення',       N'Резервні копії та відновлення даних'),
(N'TOP-008', N'Оновлення',         N'Проблеми після встановлення апдейтів'),
(N'TOP-009', N'SSO',               N'Налаштування Single Sign-On (SAML/OAuth)'),
(N'TOP-010', N'Webhooks',          N'Не доходять або дублюються вебхуки'),
(N'TOP-011', N'Локалізація',       N'Проблеми з перекладами та форматами дат'),
(N'TOP-012', N'Експорт/Імпорт',    N'Помилки при завантаженні CSV/Excel файлів'),
(N'TOP-013', N'Спам/Блокування',   N'Блокування листів або підозріла активність'),
(N'TOP-014', N'2FA',               N'Втрата доступу до двофакторної автентифікації'),
(N'TOP-015', N'Мобільний додаток', N'Краші або баги в iOS/Android додатку'),
(N'TOP-016', N'UI/UX',             N'Помилки відображення інтерфейсу (CSS/HTML)'),
(N'TOP-017', N'GDPR',              N'Запити на видалення або вивантаження персональних даних'),
(N'TOP-018', N'Ліцензії',          N'Перевищення лімітів користувачів/ресурсів'),
(N'TOP-019', N'CRM',               N'Помилки синхронізації з Salesforce/HubSpot'),
(N'TOP-020', N'Безпека',           N'Підозра на злам акаунта, вразливості');
"""

PROMPT_BLOCKS = """
INSERT INTO prompt_block ([text], version, added_by) VALUES
(N'Оціни технічну точність відповіді',                         N'1.0', N'admin'),
(N'Оціни комунікацію з клієнтом',                              N'1.2', N'admin'),
(N'Звір відповідь з базою знань',                              N'2.0', N'qa_lead'),
(N'Перевір дотримання Tone of Voice компанії',                 N'1.0', N'qa_lead'),
(N'Оціни емпатію та клієнтоорієнтованість агента',             N'1.1', N'admin'),
(N'Перевір правильність використання текстових макросів',      N'2.0', N'qa_lead'),
(N'Оціни повноту наданого рішення',                            N'1.5', N'admin'),
(N'Перевір чи було запропоновано обхідний шлях (workaround)',  N'1.0', N'qa_lead'),
(N'Оціни швидкість та адекватність реакції на ескалацію',      N'1.0', N'admin'),
(N'Перевір наявність граматичних та стилістичних помилок',     N'1.3', N'admin');
"""

TICKETS = """
INSERT INTO ticket_sla_cache (ticket_id, status, agent_name, organization, request_type,
                              ticket_created_at, first_response_time_sec, first_response_breached,
                              handling_time, total_agent_replies, total_customer_messages, refreshed_at) VALUES
(101, N'solved',  N'Ковальчук', N'Acme',       N'question', '2026-09-30', 600,  0,    3600,  3, 3, SYSDATETIME()),
(102, N'solved',  N'Ковальчук', N'Acme',       N'incident', '2026-10-01', 1800, 1,    7200,  5, 4, SYSDATETIME()),
(103, N'open',    N'Ковальчук', N'Globex',     N'question', '2026-10-02', 300,  0,    1200,  2, 2, SYSDATETIME()),
(104, N'solved',  N'Бондар',    N'Initech',    N'incident', '2026-10-02', 900,  0,    5400,  4, 3, SYSDATETIME()),
(105, N'solved',  N'Бондар',    N'Initech',    N'problem',  '2026-10-03', 2400, 1,    9000,  6, 5, SYSDATETIME()),
(106, N'new',     N'Мороз',     N'Globex',     N'question', '2026-10-04', NULL, NULL, NULL,  0, 1, SYSDATETIME()),
(107, N'closed',  N'Шевченко',  N'Umbrella',   N'problem',  '2026-10-01', 450,  0,    15000, 8, 7, SYSDATETIME()),
(108, N'solved',  N'Ткаченко',  N'Stark Ind.', N'question', '2026-10-02', 120,  0,    800,   1, 1, SYSDATETIME()),
(109, N'open',    N'Лисенко',   N'Wayne Ent.', N'incident', '2026-10-03', 3600, 1,    NULL,  3, 4, SYSDATETIME()),
(110, N'solved',  N'Ковальчук', N'Acme',       N'task',     '2026-10-04', 800,  0,    2400,  2, 2, SYSDATETIME()),
(111, N'pending', N'Бондар',    N'Globex',     N'question', '2026-10-04', 1500, 0,    7200,  4, 4, SYSDATETIME()),
(112, N'closed',  N'Мороз',     N'Initech',    N'incident', '2026-09-25', 200,  0,    1800,  2, 1, SYSDATETIME()),
(113, N'solved',  N'Шевченко',  N'Stark Ind.', N'question', '2026-10-05', 400,  0,    1200,  1, 2, SYSDATETIME()),
(114, N'open',    N'Ткаченко',  N'Umbrella',   N'problem',  '2026-10-05', 4200, 1,    NULL,  5, 6, SYSDATETIME()),
(115, N'new',     N'Лисенко',   N'Wayne Ent.', N'task',     '2026-10-06', NULL, NULL, NULL,  0, 1, SYSDATETIME()),
(116, N'solved',  N'Ковальчук', N'Globex',     N'incident', '2026-10-06', 600,  0,    3600,  3, 3, SYSDATETIME()),
(117, N'closed',  N'Бондар',    N'Acme',       N'question', '2026-09-28', 950,  0,    4800,  4, 3, SYSDATETIME()),
(118, N'solved',  N'Мороз',     N'Initech',    N'task',     '2026-10-07', 300,  0,    900,   1, 1, SYSDATETIME()),
(119, N'open',    N'Шевченко',  N'Stark Ind.', N'incident', '2026-10-07', 2400, 1,    NULL,  2, 3, SYSDATETIME()),
(120, N'solved',  N'Ткаченко',  N'Umbrella',   N'question', '2026-10-08', 150,  0,    600,   1, 1, SYSDATETIME()),
(121, N'pending', N'Лисенко',   N'Acme',       N'problem',  '2026-10-08', 1800, 0,    12000, 6, 5, SYSDATETIME()),
(122, N'solved',  N'Ковальчук', N'Wayne Ent.', N'task',     '2026-10-09', 400,  0,    2000,  2, 2, SYSDATETIME()),
(123, N'closed',  N'Бондар',    N'Globex',     N'incident', '2026-09-29', 500,  0,    2500,  3, 2, SYSDATETIME()),
(124, N'solved',  N'Мороз',     N'Initech',    N'question', '2026-10-09', 700,  0,    1400,  2, 2, SYSDATETIME()),
(125, N'new',     NULL,         N'Stark Ind.', N'problem',  '2026-10-10', NULL, NULL, NULL,  0, 1, SYSDATETIME()),
(126, N'solved',  N'Ткаченко',  N'Umbrella',   N'incident', '2026-10-10', 360,  0,    1800,  2, 2, SYSDATETIME()),
(127, N'open',    N'Лисенко',   N'Globex',     N'task',     '2026-10-11', 1200, 0,    NULL,  1, 2, SYSDATETIME()),
(128, N'solved',  N'Ковальчук', N'Acme',       N'question', '2026-10-11', 250,  0,    800,   1, 1, SYSDATETIME()),
(129, N'pending', N'Бондар',    N'Wayne Ent.', N'incident', '2026-10-11', 3200, 1,    9500,  5, 5, SYSDATETIME()),
(130, N'solved',  N'Шевченко',  N'Initech',    N'problem',  '2026-10-11', 600,  0,    7200,  4, 4, SYSDATETIME());
"""

# 40 оцінок, qa_evaluation_id = 1..40
QA_EVALUATIONS = """
INSERT INTO qa_evaluation (canonical_topic_id, ticket_id, result, overall_score, organization_name, llm_model, created_at) VALUES
(1,  101,  N'pass',    8.5,  N'Acme',       N'gpt-x', '2026-10-01 10:00'),  -- 1
(2,  101,  N'pass',    9.0,  N'Acme',       N'gpt-x', '2026-10-01 11:00'),  -- 2
(1,  102,  N'fail',    4.5,  N'Acme',       N'gpt-x', '2026-10-02 09:30'),  -- 3
(2,  102,  N'pass',    7.0,  N'Acme',       N'gpt-x', '2026-10-02 12:00'),  -- 4
(3,  103,  N'pass',    9.5,  N'Globex',     N'gpt-x', '2026-10-03 10:15'),  -- 5
(1,  104,  N'pass',    8.0,  N'Initech',    N'gpt-x', '2026-10-03 14:00'),  -- 6
(1,  105,  N'fail',    5.0,  N'Initech',    N'gpt-x', '2026-10-04 09:00'),  -- 7
(4,  105,  N'pass',    6.5,  N'Initech',    N'gpt-x', '2026-10-04 15:00'),  -- 8
(3,  NULL, N'pass',    7.5,  N'Globex',     N'gpt-x', '2026-10-05 10:00'),  -- 9
(6,  107,  N'pass',    8.0,  N'Umbrella',   N'gpt-x', '2026-10-02 14:00'),  -- 10
(7,  108,  N'pass',    9.5,  N'Stark Ind.', N'gpt-x', '2026-10-03 10:00'),  -- 11
(8,  109,  N'fail',    4.0,  N'Wayne Ent.', N'gpt-x', '2026-10-04 11:30'),  -- 12
(9,  110,  N'pass',    8.5,  N'Acme',       N'gpt-x', '2026-10-05 09:15'),  -- 13
(10, 111,  N'partial', 6.5,  N'Globex',     N'gpt-x', '2026-10-05 16:20'),  -- 14
(11, 112,  N'pass',    9.0,  N'Initech',    N'gpt-x', '2026-09-26 12:00'),  -- 15
(12, 113,  N'pass',    10.0, N'Stark Ind.', N'gpt-x', '2026-10-06 14:45'),  -- 16
(13, 114,  N'fail',    3.5,  N'Umbrella',   N'gpt-x', '2026-10-06 17:00'),  -- 17
(14, 116,  N'pass',    7.5,  N'Globex',     N'gpt-x', '2026-10-07 10:10'),  -- 18
(15, 117,  N'pass',    8.8,  N'Acme',       N'gpt-x', '2026-09-29 11:00'),  -- 19
(16, 118,  N'pass',    9.2,  N'Initech',    N'gpt-x', '2026-10-08 09:30'),  -- 20
(17, 119,  N'partial', 5.5,  N'Stark Ind.', N'gpt-x', '2026-10-08 13:20'),  -- 21
(18, 120,  N'pass',    9.8,  N'Umbrella',   N'gpt-x', '2026-10-09 10:00'),  -- 22
(19, 121,  N'partial', 6.0,  N'Acme',       N'gpt-x', '2026-10-09 15:45'),  -- 23
(20, 122,  N'pass',    8.5,  N'Wayne Ent.', N'gpt-x', '2026-10-10 11:15'),  -- 24
(1,  123,  N'pass',    9.0,  N'Globex',     N'gpt-x', '2026-09-30 14:00'),  -- 25
(2,  124,  N'pass',    7.8,  N'Initech',    N'gpt-x', '2026-10-10 16:30'),  -- 26
(3,  126,  N'pass',    8.2,  N'Umbrella',   N'gpt-x', '2026-10-11 09:00'),  -- 27
(4,  127,  N'fail',    4.5,  N'Globex',     N'gpt-x', '2026-10-11 10:30'),  -- 28
(5,  128,  N'pass',    9.5,  N'Acme',       N'gpt-x', '2026-10-11 11:00'),  -- 29
(6,  129,  N'partial', 5.0,  N'Wayne Ent.', N'gpt-x', '2026-10-11 12:45'),  -- 30
(7,  130,  N'pass',    8.9,  N'Initech',    N'gpt-x', '2026-10-11 14:15'),  -- 31
(8,  107,  N'partial', 6.5,  N'Umbrella',   N'gpt-x', '2026-10-02 15:00'),  -- 32
(9,  108,  N'pass',    9.0,  N'Stark Ind.', N'gpt-x', '2026-10-03 10:30'),  -- 33
(10, 109,  N'fail',    3.0,  N'Wayne Ent.', N'gpt-x', '2026-10-04 12:00'),  -- 34
(11, 110,  N'pass',    8.0,  N'Acme',       N'gpt-x', '2026-10-05 09:45'),  -- 35
(12, 111,  N'pass',    7.5,  N'Globex',     N'gpt-x', '2026-10-05 17:00'),  -- 36
(13, 112,  N'pass',    9.5,  N'Initech',    N'gpt-x', '2026-09-26 12:30'),  -- 37
(14, 113,  N'pass',    9.8,  N'Stark Ind.', N'gpt-x', '2026-10-06 15:00'),  -- 38
(15, 114,  N'fail',    4.0,  N'Umbrella',   N'gpt-x', '2026-10-06 17:30'),  -- 39
(16, 116,  N'pass',    8.5,  N'Globex',     N'gpt-x', '2026-10-07 10:45');  -- 40
"""

QA_EVALUATION_PROMPT_BLOCKS = """
INSERT INTO qa_evaluation_prompt_block (prompt_block_id, qa_evaluation_id) VALUES
(1,1),(2,1),(3,2),(1,3),(2,5),(3,6),
(4,10),(5,10),(6,10),
(7,11),(8,11),(9,11),
(10,12),(1,12),(2,12),
(3,13),(4,13),(5,13),
(6,14),(7,14),(8,14),
(9,15),(10,15),(1,15),
(2,16),(3,16),(4,16),
(5,17),(6,17),(7,17),
(8,18),(9,18),(10,18),
(1,19),(2,19),(3,19),
(4,20),(5,20),(6,20),
(7,21),(8,21),(9,21),
(10,22),(1,22),(2,22),
(3,23),(4,23),(5,23),
(6,24),(7,24),(8,24),
(9,25),(10,25),(1,25),
(2,26),(3,26),(4,26),
(5,27),(6,27),(7,27),
(8,28),(9,28),(10,28),
(1,29),(2,29),(3,29),
(4,30),(5,30),(6,30),
(7,31),(8,31),(9,31),
(10,32),(1,32),(2,32),
(3,33),(4,33),(5,33),
(6,34),(7,34),(8,34),
(9,35),(10,35),(1,35),
(2,36),(3,36),(4,36),
(5,37),(6,37),(7,37),
(8,38),(9,38),(10,38),
(1,39),(2,39),(3,39),
(4,40),(5,40),(6,40);
"""

IDENTITY_TABLES = (
    "qa_evaluation_prompt_block",
    "qa_evaluation",
    "prompt_block",
    "canonical_topics",
)


def upgrade() -> None:
    for sql in (
        CANONICAL_TOPICS,
        PROMPT_BLOCKS,
        TICKETS,
        QA_EVALUATIONS,
        QA_EVALUATION_PROMPT_BLOCKS,
    ):
        _execute(sql)


def downgrade() -> None:
    _execute("DELETE FROM qa_evaluation_prompt_block;")
    _execute("DELETE FROM qa_evaluation;")
    _execute("DELETE FROM ticket_sla_cache;")
    _execute("DELETE FROM prompt_block;")
    _execute("DELETE FROM canonical_topics;")
    # щоб повторний upgrade знову дав id 1..N
    for table in IDENTITY_TABLES:
        _execute(f"DBCC CHECKIDENT ('{table}', RESEED, 0);")
