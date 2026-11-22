# QA_Support backend

FastAPI + async SQLAlchemy (`mssql+aioodbc`) + Alembic. Схема БД ЛР1–ЛР2 відтворюється лише міграціями.

## Міграції

| Ревізія | Що робить |
|---|---|
| `0001` | ЛР1, дод. А — 5 таблиць, PK/FK/UNIQUE з оригінальними назвами |
| `0002` | ЛР1, дод. Б — початкові дані (20 тем, 10 блоків, 30 тікетів, 40 оцінок, 99 звʼязків) |
| `0003` | ЛР1, дод. В–Е — `TOP_TOPIC_BY_AGENT_NAME`, `SET_TOPIC_PRIORITY`, `MAX_EVALUATION_BY_TOPIC`, `SET_TOP_ORGANIZATION_FOR_TOPIC` |
| `0004` | ЛР2 — `qa_evaluation_copy`, `tags` → `NVARCHAR(MAX)`, тригери `tr_qa_evaluation_copy_score`, `tr_qa_evaluation_add_to_ticket` |

Дані йдуть до тригерів, тому початкові INSERT-и не пишуть номери оцінок у `tags`.

## Запуск у Docker (нічого, крім Docker, не потрібно)

```bash
# з кореня labo_3
cp .env.example .env            # пароль sa
docker compose up -d --build    # SQL Server 2022 + API; API сам створює БД і робить upgrade head
# http://localhost:8000/docs
```

Скинути БД до чистого стану: `docker compose down -v && docker compose up -d`.

## Локально (потрібен ODBC Driver 18 for SQL Server)

```bash
cd backend
cp .env.example .env
docker compose up -d db                 # або власний SQL Server
uv run python -m app.scripts.create_database
uv run alembic upgrade head
uv run fastapi dev app/main.py
uv run pytest
```

## Корисне

```bash
uv run alembic upgrade head --sql > qa_support.sql   # SQL-скрипт з GO для DBeaver/sqlcmd, без підключення
uv run alembic revision --autogenerate -m "..."      # нова міграція після зміни моделей; файл ОБОВʼЯЗКОВО переглянути
uv run alembic check                                 # моделі == БД
uv run alembic downgrade -1
```

Функції, процедури й тригери autogenerate не бачить: їх пишемо в міграції вручну через `op.execute`.
