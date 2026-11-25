// Типи відповідають pydantic-схемам бекенду. Decimal приходить рядком.

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface TicketBrief {
  ticket_id: number;
  status: string | null;
  agent_name: string | null;
  organization: string | null;
  request_type: string | null;
}

export interface Ticket extends TicketBrief {
  tags: string | null;
  ticket_created_at: string | null;
  ticket_updated_at: string | null;
  first_response_time_sec: number | null;
  first_response_breached: boolean | null;
  handling_time: number | null;
  longest_agent_gap_sec: number | null;
  avg_gap_sec: number | null;
  agent_gap_sec: number | null;
  agent_gap_breached: boolean | null;
  longest_customer_gap_sec: number | null;
  avg_customer_gap_sec: number | null;
  total_agent_replies: number | null;
  total_customer_messages: number | null;
  refreshed_at: string | null;
}

export interface TopicBrief {
  canonical_topic_id: number;
  topic_id: string;
  topic_label: string;
}

export interface Topic extends TopicBrief {
  meaning: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
  synonyms: string | null;
  client_aliases: string | null;
  related_terms: string | null;
}

export interface PromptBlock {
  prompt_block_id: number;
  text: string | null;
  version: string | null;
  added_by: string | null;
  created_at: string;
}

export interface EvaluationListItem {
  qa_evaluation_id: number;
  result: string | null;
  overall_score: string | null;
  organization_name: string | null;
  llm_model: string | null;
  created_at: string;
  topic: TopicBrief | null;
  ticket: TicketBrief | null;
}

export interface EvaluationDetail {
  qa_evaluation_id: number;
  result: string | null;
  overall_score: string | null;
  kb_source_title: string | null;
  kb_source_url: string | null;
  correct_points: string | null;
  missing_points: string | null;
  incorrect_points: string | null;
  communication_issues: string | null;
  qa_comment: string | null;
  recommendation: string | null;
  raw_issue_topic: string | null;
  llm_model: string | null;
  created_at: string;
  updated_at: string | null;
  organization_name: string | null;
  topic_confidence: string | null;
  technical_accuracy_score: string | null;
  troubleshooting_approach_score: string | null;
  completeness_score: string | null;
  case_ownership_score: string | null;
  technical_quality_score: string | null;
  communication_quality_score: string | null;
  topic: Topic | null;
  ticket: Ticket | null;
  prompt_blocks: PromptBlock[];
}

export interface MaxEvaluationRow {
  qa_evaluation_id: number | null;
  ticket_id: number | null;
  overall_score: string | null;
  result: string | null;
  created_at: string | null;
  info: string | null;
}

/** Помилка API. Для THROW/RAISERROR (номер ≥ 50000) бекенд віддає source = "database". */
export class ApiError extends Error {
  status: number;
  source?: string;
  errorNumber?: number;

  constructor(status: number, message: string, source?: string, errorNumber?: number) {
    super(message);
    this.status = status;
    this.source = source;
    this.errorNumber = errorNumber;
  }

  get isDatabaseError(): boolean {
    return this.source === "database";
  }
}

type Query = Record<string, string | number | boolean | null | undefined>;

async function request<T>(path: string, init?: RequestInit & { query?: Query }): Promise<T> {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(init?.query ?? {})) {
    if (value !== undefined && value !== null && value !== "") params.set(key, String(value));
  }
  const qs = params.size ? `?${params}` : "";

  const res = await fetch(`/api/v1${path}${qs}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  const body = await res.json().catch(() => null);

  if (!res.ok) {
    const detail = body?.detail;
    // 422 від FastAPI: detail — масив помилок валідації
    const message = Array.isArray(detail)
      ? detail.map((d: { loc?: string[]; msg: string }) => `${d.loc?.at(-1) ?? ""}: ${d.msg}`).join("; ")
      : (detail ?? `HTTP ${res.status}`);
    throw new ApiError(res.status, message, body?.source, body?.error_number);
  }
  return body as T;
}

const enc = encodeURIComponent;

export const api = {
  health: () => request<{ status: string; database: string }>("/health"),

  // Таблиці
  tickets: (query: Query) => request<Page<Ticket>>("/tickets", { query }),
  ticket: (id: string | number) => request<Ticket>(`/tickets/${id}`),
  agents: () => request<string[]>("/tickets/agents"),
  topics: (query: Query) => request<Page<Topic>>("/topics", { query }),
  topic: (id: string | number) => request<Topic>(`/topics/${id}`),
  promptBlocks: (query: Query) => request<Page<PromptBlock>>("/prompt-blocks", { query }),
  evaluations: (query: Query) => request<Page<EvaluationListItem>>("/evaluations", { query }),
  evaluation: (id: string | number) => request<EvaluationDetail>(`/evaluations/${id}`),

  // Скалярна функція req_count_by_agnet_NAME
  evaluatedTicketsCount: (agent: string) =>
    request<{ agent_name: string; evaluated_tickets: number }>(
      `/tickets/agents/${enc(agent)}/evaluated-tickets-count`,
    ),
  // Таблична функція TOP_TOPIC_BY_AGENT_NAME
  topTopicsByAgent: (agent: string) =>
    request<{ agent_name: string; topic_labels: string[] }>("/topics/top-by-agent", {
      query: { agent_name: agent },
    }),
  // Таблична функція MAX_EVALUATION_BY_TOPIC
  maxEvaluationByTopic: (topicLabel: string) =>
    request<{ topic_label: string; items: MaxEvaluationRow[] }>("/evaluations/max-by-topic", {
      query: { topic_label: topicLabel },
    }),

  // Процедура SET_TOPIC_PRIORITY
  setTopicPriority: (topic_label: string, priority_percent: number) =>
    request<Topic>("/topics/priority", {
      method: "POST",
      body: JSON.stringify({ topic_label, priority_percent }),
    }),
  // Процедура SET_TOP_ORGANIZATION_FOR_TOPIC
  setTopOrganization: (topic_label: string) =>
    request<Topic>("/topics/top-organization", {
      method: "POST",
      body: JSON.stringify({ topic_label }),
    }),
};
