from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class PromptBlock(Base):
    __tablename__ = "prompt_block"

    prompt_block_id: Mapped[int] = mapped_column(
        sa.Integer, sa.Identity(start=1, increment=1), primary_key=True
    )
    text: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    version: Mapped[str | None] = mapped_column(sa.Unicode(20), nullable=True)
    added_by: Mapped[str | None] = mapped_column(sa.Unicode(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME2, server_default=sa.text("SYSDATETIME()"), nullable=False
    )
