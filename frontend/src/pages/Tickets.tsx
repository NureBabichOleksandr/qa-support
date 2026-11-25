import { Link, useParams } from "react-router";
import { api } from "../api";
import { RelatedEvaluations } from "../components/EvaluationsTable";
import { Async, Card, Fields, FilterInput, Pagination } from "../components/ui";
import { fmtBool, fmtDate, fmtSec, text } from "../format";
import { useFetch, useQueryState } from "../hooks";

export function TicketsPage() {
  const q = useQueryState();
  const filters = { agent_name: q.get("agent_name"), status: q.get("status"), organization: q.get("organization") };
  const agents = useFetch(api.agents, []);
  const state = useFetch(() => api.tickets({ ...filters, page: q.page }), [JSON.stringify(filters), q.page]);

  return (
    <>
      <h1>Тікети</h1>
      <div className="filters">
        <select value={filters.agent_name} onChange={(e) => q.set("agent_name", e.target.value)}>
          <option value="">Усі агенти</option>
          {agents.data?.map((a) => <option key={a}>{a}</option>)}
        </select>
        <FilterInput placeholder="Статус" value={filters.status} onApply={(v) => q.set("status", v)} />
        <FilterInput placeholder="Організація" value={filters.organization} onApply={(v) => q.set("organization", v)} />
      </div>
      <Card>
        <Async state={state}>
          {(page) => (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Тікет</th>
                    <th>Статус</th>
                    <th>Агент</th>
                    <th>Організація</th>
                    <th>Тип запиту</th>
                    <th>Перша відповідь</th>
                    <th>Створено</th>
                  </tr>
                </thead>
                <tbody>
                  {page.items.map((t) => (
                    <tr key={t.ticket_id}>
                      <td>
                        <Link to={`/tickets/${t.ticket_id}`}>{t.ticket_id}</Link>
                      </td>
                      <td>{text(t.status)}</td>
                      <td>
                        {t.agent_name ? (
                          <Link to={`/agents/${encodeURIComponent(t.agent_name)}`}>{t.agent_name}</Link>
                        ) : (
                          "—"
                        )}
                      </td>
                      <td>{text(t.organization)}</td>
                      <td>{text(t.request_type)}</td>
                      <td className={t.first_response_breached ? "danger" : ""}>{fmtSec(t.first_response_time_sec)}</td>
                      <td>{fmtDate(t.ticket_created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <Pagination page={page.page} totalPages={page.total_pages} total={page.total} onChange={q.setPage} />
            </>
          )}
        </Async>
      </Card>
    </>
  );
}

/** Тікет (одна картка, без дублювання) + усі його оцінки. */
export function TicketPage() {
  const id = useParams().id!;
  const state = useFetch(() => api.ticket(id), [id]);

  return (
    <>
      <p className="crumbs">
        <Link to="/tickets">Тікети</Link> /
      </p>
      <h1>Тікет #{id}</h1>
      <Async state={state}>
        {(t) => (
          <Card>
            <Fields
              items={[
                ["Статус", text(t.status)],
                [
                  "Агент",
                  t.agent_name ? <Link to={`/agents/${encodeURIComponent(t.agent_name)}`}>{t.agent_name}</Link> : "—",
                ],
                ["Організація", text(t.organization)],
                ["Тип запиту", text(t.request_type)],
                ["Теги", text(t.tags)],
                ["Створено", fmtDate(t.ticket_created_at)],
                ["Оновлено", fmtDate(t.ticket_updated_at)],
                ["Перша відповідь", fmtSec(t.first_response_time_sec)],
                ["SLA першої відповіді порушено", fmtBool(t.first_response_breached)],
                ["Час обробки", fmtSec(t.handling_time)],
                ["Найдовша пауза агента", fmtSec(t.longest_agent_gap_sec)],
                ["Середня пауза", fmtSec(t.avg_gap_sec)],
                ["Пауза агента", fmtSec(t.agent_gap_sec)],
                ["SLA паузи агента порушено", fmtBool(t.agent_gap_breached)],
                ["Найдовша пауза клієнта", fmtSec(t.longest_customer_gap_sec)],
                ["Середня пауза клієнта", fmtSec(t.avg_customer_gap_sec)],
                ["Відповідей агента", text(t.total_agent_replies)],
                ["Повідомлень клієнта", text(t.total_customer_messages)],
              ]}
            />
          </Card>
        )}
      </Async>
      <Card title="Оцінки тікета">
        <RelatedEvaluations filter={{ ticket_id: id }} hide={["ticket", "agent"]} />
      </Card>
    </>
  );
}
