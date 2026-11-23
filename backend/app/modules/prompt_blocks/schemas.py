from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PromptBlockRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prompt_block_id: int
    text: str | None
    version: str | None
    added_by: str | None
    created_at: datetime
