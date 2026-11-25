import { Link, useParams } from "react-router";
import { api } from "../api";
import { EvaluationsTable } from "../components/EvaluationsTable";
import { Async, Card, Fields, Pagination, ResultBadge } from "../components/ui";
import { fmtBool, fmtDate, fmtScore, fmtSec, text } from "../format";
import { useFetch, useQueryState } from "../hooks";

export function EvaluationsPage() {
  const q = useQueryState();
  const filters = { agent_name: q.get("agent_name"), result: q.get("result") };
  const agents = useFetch(api.agents, []);
  const state = useFetch(() => api.evaluations({ ...filters, page: q.page }), [JSON.stringify(filters), q.page]);

  return (
    <>
      <h1>Оцінки якості</h1>
      <div className="filters">
        <select value={filters.agent_name} onChange={(e) => q.set("agent_name", e.target.value)}>
          <option value="">Усі агенти</option>
          {agents.data?.map((a) => <option key={a}>{a}</option>)}
        </select>
        <select value={filters.result} onChange={(e) => q.set("result", e.target.value)}>
          <option value="">Усі результати</option>
          <option value="pass">pass</option>
          <option value="partial">partial</option>
          <option value="fail">fail</option>
        </select>
      </div>
      <Card>
        <Async state={state}>
          {(page) => (
            <>
              <EvaluationsTable items={page.items} />
              <Pagination page={page.page} totalPages={page.total_pages} total={page.total} onChange={q.setPage} />
            </>
          )}
        </Async>
      </Card>
    </>
  );
}

/** Оцінка разом з повʼязаними темою, тікетом і блоками промпту (M:N). */
export function EvaluationPage() {
  const id = useParams().id!;
  const state = useFetch(() => api.evaluation(id), [id]);

  return (
    <>
      <p className="crumbs">
        <Link to="/evaluations">Оцінки</Link> /
      </p>
      <Async state={state}>
        {(e) => (
          <>
            <h1>
              Оцінка #{e.qa_evaluation_id} <ResultBadge result={e.result} />
            </h1>

            <Card title="Бали">
              <div className="scores">
                {(
                  [
                    ["Загальний", e.overall_score],
                    ["Технічна точність", e.technical_accuracy_score],
                    ["Траблшутинг", e.troubleshooting_approach_score],
                    ["Повнота", e.completeness_score],
                    ["Відповідальність за кейс", e.case_ownership_score],
                    ["Технічна якість", e.technical_quality_score],
                    ["Якість комунікації", e.communication_quality_score],
                  ] as const
                ).map(([label, value]) => (
                  <div key={label} className="score">
                    <div className="score-value">{fmtScore(value)}</div>
                    <div className="small muted">{label}</div>
                  </div>
                ))}
              </div>
            </Card>

            <Card title="Висновки QA">
              <Fields
                items={[
                  ["Коментар QA", text(e.qa_comment)],
                  ["Рекомендація", text(e.recommendation)],
                  ["Правильно", text(e.correct_points)],
                  ["Пропущено", text(e.missing_points)],
                  ["Неправильно", text(e.incorrect_points)],
                  ["Проблеми комунікації", text(e.communication_issues)],
                  [
                    "Джерело в KB",
                    e.kb_source_url ? (
                      <a href={e.kb_source_url} target="_blank" rel="noreferrer">
                        {e.kb_source_title ?? e.kb_source_url}
                      </a>
                    ) : (
                      text(e.kb_source_title)
                    ),
                  ],
                  ["Сира тема звернення", text(e.raw_issue_topic)],
                  ["Організація", text(e.organization_name)],
                  ["LLM-модель", text(e.llm_model)],
                  ["Впевненість у темі", fmtScore(e.topic_confidence)],
                  ["Створено", fmtDate(e.created_at)],
                ]}
              />
            </Card>

            <div className="grid-2">
              <Card title="Тема">
                {e.topic ? (
                  <Fields
                    items={[
                      [
                        "Назва",
                        <Link to={`/topics/${e.topic.canonical_topic_id}`}>
                          {e.topic.topic_label} ({e.topic.topic_id})
                        </Link>,
                      ],
                      ["Опис", text(e.topic.meaning)],
                      ["Активна", fmtBool(e.topic.is_active)],
                    ]}
                  />
                ) : (
                  <p className="muted">Без теми</p>
                )}
              </Card>
              <Card title="Тікет">
                {e.ticket ? (
                  <Fields
                    items={[
                      ["Номер", <Link to={`/tickets/${e.ticket.ticket_id}`}>#{e.ticket.ticket_id}</Link>],
                      [
                        "Агент",
                        e.ticket.agent_name ? (
                          <Link to={`/agents/${encodeURIComponent(e.ticket.agent_name)}`}>{e.ticket.agent_name}</Link>
                        ) : (
                          "—"
                        ),
                      ],
                      ["Статус", text(e.ticket.status)],
                      ["Перша відповідь", fmtSec(e.ticket.first_response_time_sec)],
                    ]}
                  />
                ) : (
                  <p className="muted">Без тікета</p>
                )}
              </Card>
            </div>

            <Card title={`Блоки промпту (${e.prompt_blocks.length})`}>
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Текст</th>
                    <th>Версія</th>
                    <th>Автор</th>
                  </tr>
                </thead>
                <tbody>
                  {e.prompt_blocks.map((b) => (
                    <tr key={b.prompt_block_id}>
                      <td>{b.prompt_block_id}</td>
                      <td>{text(b.text)}</td>
                      <td>{text(b.version)}</td>
                      <td>{text(b.added_by)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </>
        )}
      </Async>
    </>
  );
}
