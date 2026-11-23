from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TopicBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    canonical_topic_id: int
    topic_id: str
    topic_label: str


class TopicRead(TopicBrief):

    meaning: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    synonyms: str | None
    client_aliases: str | None
    related_terms: str | None


class TopicFilterParams(BaseModel):
    search: str | None = Field(None, description="Частина назви теми")
    is_active: bool | None = None


class TopicPriorityRequest(BaseModel):
    topic_label: str = Field(examples=["Біллінг"])
    priority_percent: int = Field(ge=0, le=100, examples=[20])


class TopOrganizationRequest(BaseModel):
    topic_label: str = Field(examples=["Інтеграції"])


class TopTopicsByAgentResponse(BaseModel):
    agent_name: str
    topic_labels: list[str]
