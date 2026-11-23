from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.modules.prompt_blocks.schemas import PromptBlockRead
from app.modules.tickets.schemas import TicketBrief, TicketRead
from app.modules.topics.schemas import TopicBrief, TopicRead


class EvaluationListItem(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    qa_evaluation_id: int
    result: str | None
    overall_score: Decimal | None
    organization_name: str | None
    llm_model: str | None
    created_at: datetime
    topic: TopicBrief | None
    ticket: TicketBrief | None


class EvaluationDetail(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    qa_evaluation_id: int
    result: str | None
    overall_score: Decimal | None
    kb_source_title: str | None
    kb_source_url: str | None
    correct_points: str | None
    missing_points: str | None
    incorrect_points: str | None
    communication_issues: str | None
    qa_comment: str | None
    recommendation: str | None
    raw_issue_topic: str | None
    llm_model: str | None
    created_at: datetime
    updated_at: datetime | None
    organization_name: str | None
    topic_confidence: Decimal | None
    technical_accuracy_score: Decimal | None
    troubleshooting_approach_score: Decimal | None
    completeness_score: Decimal | None
    case_ownership_score: Decimal | None
    technical_quality_score: Decimal | None
    communication_quality_score: Decimal | None
    topic: TopicRead | None
    ticket: TicketRead | None
    prompt_blocks: list[PromptBlockRead]


class EvaluationFilterParams(BaseModel):
    canonical_topic_id: int | None = None
    ticket_id: int | None = None
    agent_name: str | None = Field(None, description="Агент тікета")
    result: str | None = Field(None, examples=["pass"])


class MaxEvaluationRow(BaseModel):

    qa_evaluation_id: int | None
    ticket_id: int | None
    overall_score: Decimal | None
    result: str | None
    created_at: datetime | None
    info: str | None


class MaxEvaluationByTopicResponse(BaseModel):
    topic_label: str
    items: list[MaxEvaluationRow]
