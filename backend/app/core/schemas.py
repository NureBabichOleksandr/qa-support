from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str


class Page[T](BaseModel):
    items: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    total_pages: int = Field(ge=1)
