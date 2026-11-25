import { Link } from "react-router";
import { api, type EvaluationListItem } from "../api";
import { fmtDate, fmtScore, text } from "../format";
import { useFetch } from "../hooks";
import { Async, ResultBadge } from "./ui";

type Column = "topic" | "ticket" | "agent";

export function EvaluationsTable({
  items,
  hide = [],
}: {
  items: EvaluationListItem[];
  hide?: Column[];
}) {
  if (!items.length) return <p className="muted">Оцінок немає</p>;
  const show = (c: Column) => !hide.includes(c);

  return (
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Результат</th>
          <th>Бал</th>
          {show("topic") && <th>Тема</th>}
          {show("ticket") && <th>Тікет</th>}
          {show("agent") && <th>Агент</th>}
          <th>Організація</th>
          <th>Створено</th>
        </tr>
      </thead>
      <tbody>
        {items.map((e) => (
          <tr key={e.qa_evaluation_id}>
            <td>
              <Link to={`/evaluations/${e.qa_evaluation_id}`}>{e.qa_evaluation_id}</Link>
            </td>
            <td>
              <ResultBadge result={e.result} />
            </td>
            <td>{fmtScore(e.overall_score)}</td>
            {show("topic") && (
              <td>
                {e.topic ? (
                  <Link to={`/topics/${e.topic.canonical_topic_id}`}>{e.topic.topic_label}</Link>
                ) : (
                  "—"
                )}
              </td>
            )}
            {show("ticket") && (
              <td>
                {e.ticket ? <Link to={`/tickets/${e.ticket.ticket_id}`}>{e.ticket.ticket_id}</Link> : "—"}
              </td>
            )}
            {show("agent") && (
              <td>
                {e.ticket?.agent_name ? (
                  <Link to={`/agents/${encodeURIComponent(e.ticket.agent_name)}`}>{e.ticket.agent_name}</Link>
                ) : (
                  "—"
                )}
              </td>
            )}
            <td>{text(e.organization_name)}</td>
            <td>{fmtDate(e.created_at)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function RelatedEvaluations({
  filter,
  hide,
}: {
  filter: Record<string, string | number>;
  hide?: Column[];
}) {
  const state = useFetch(() => api.evaluations({ ...filter, limit: 100 }), [JSON.stringify(filter)]);
  return <Async state={state}>{(page) => <EvaluationsTable items={page.items} hide={hide} />}</Async>;
}
