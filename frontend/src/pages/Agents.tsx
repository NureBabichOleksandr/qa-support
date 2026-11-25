import { Link, useParams } from "react-router";
import { api } from "../api";
import { RelatedEvaluations } from "../components/EvaluationsTable";
import { Async, Card } from "../components/ui";
import { text } from "../format";
import { useFetch } from "../hooks";

export function AgentsPage() {
  const state = useFetch(api.agents, []);
  return (
    <>
      <h1>Агенти підтримки</h1>
      <Card>
        <Async state={state}>
          {(agents) => (
            <table>
              <thead>
                <tr>
                  <th>Агент</th>
                  <th>Оцінених тікетів</th>
                </tr>
              </thead>
              <tbody>
                {agents.map((name) => (
                  <tr key={name}>
                    <td>
                      <Link to={`/agents/${encodeURIComponent(name)}`}>{name}</Link>
                    </td>
                    <td>
                      <EvaluatedCount agent={name} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Async>
      </Card>
    </>
  );
}

/** Скалярна функція req_count_by_agnet_NAME для одного агента. */
function EvaluatedCount({ agent }: { agent: string }) {
  const state = useFetch(() => api.evaluatedTicketsCount(agent), [agent]);
  if (state.error) return <span className="muted">помилка</span>;
  return <>{state.data?.evaluated_tickets ?? "…"}</>;
}

export function AgentPage() {
  const name = useParams().name!;
  const count = useFetch(() => api.evaluatedTicketsCount(name), [name]);
  const topTopics = useFetch(() => api.topTopicsByAgent(name), [name]);
  const tickets = useFetch(() => api.tickets({ agent_name: name, limit: 100 }), [name]);

  return (
    <>
      <p className="crumbs">
        <Link to="/agents">Агенти</Link> /
      </p>
      <h1>{name}</h1>

      <div className="grid-2">
        <Card title="Оцінених тікетів">
          <p className="small muted">скалярна функція req_count_by_agnet_NAME</p>
          <Async state={count}>{(d) => <div className="big-number">{d.evaluated_tickets}</div>}</Async>
        </Card>
        <Card title="Найчастіші теми">
          <p className="small muted">таблична функція TOP_TOPIC_BY_AGENT_NAME</p>
          <Async state={topTopics}>
            {(d) => (
              <ul className="chips">
                {d.topic_labels.map((label) => (
                  <li key={label}>{label}</li>
                ))}
              </ul>
            )}
          </Async>
        </Card>
      </div>

      <Card title="Тікети агента">
        <Async state={tickets}>
          {(page) => (
            <table>
              <thead>
                <tr>
                  <th>Тікет</th>
                  <th>Статус</th>
                  <th>Організація</th>
                  <th>Тип запиту</th>
                </tr>
              </thead>
              <tbody>
                {page.items.map((t) => (
                  <tr key={t.ticket_id}>
                    <td>
                      <Link to={`/tickets/${t.ticket_id}`}>{t.ticket_id}</Link>
                    </td>
                    <td>{text(t.status)}</td>
                    <td>{text(t.organization)}</td>
                    <td>{text(t.request_type)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Async>
      </Card>

      <Card title="Оцінки агента">
        <RelatedEvaluations filter={{ agent_name: name }} hide={["agent"]} />
      </Card>
    </>
  );
}
