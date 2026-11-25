import { Link, useParams } from "react-router";
import { api, type MaxEvaluationRow } from "../api";
import { RelatedEvaluations } from "../components/EvaluationsTable";
import { PriorityForm, TopOrganizationForm } from "../components/TopicForms";
import { Async, Card, Fields, FilterInput, Pagination, ResultBadge } from "../components/ui";
import { fmtBool, fmtDate, fmtScore, text } from "../format";
import { useFetch, useQueryState } from "../hooks";

export function TopicsPage() {
  const q = useQueryState();
  const filters = { search: q.get("search"), is_active: q.get("is_active") };
  const state = useFetch(() => api.topics({ ...filters, page: q.page }), [JSON.stringify(filters), q.page]);

  return (
    <>
      <h1>Теми звернень</h1>
      <div className="filters">
        <FilterInput placeholder="Пошук за назвою" value={filters.search} onApply={(v) => q.set("search", v)} />
        <select value={filters.is_active} onChange={(e) => q.set("is_active", e.target.value)}>
          <option value="">Усі</option>
          <option value="true">Активні</option>
          <option value="false">Неактивні</option>
        </select>
      </div>
      <Card>
        <Async state={state}>
          {(page) => (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Код</th>
                    <th>Назва</th>
                    <th>Опис (meaning)</th>
                    <th>Повʼязані терміни</th>
                    <th>Активна</th>
                  </tr>
                </thead>
                <tbody>
                  {page.items.map((t) => (
                    <tr key={t.canonical_topic_id}>
                      <td>{t.topic_id}</td>
                      <td>
                        <Link to={`/topics/${t.canonical_topic_id}`}>{t.topic_label}</Link>
                      </td>
                      <td>{text(t.meaning)}</td>
                      <td>{text(t.related_terms)}</td>
                      <td>{fmtBool(t.is_active)}</td>
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

export function TopicPage() {
  const id = useParams().id!;
  const state = useFetch(() => api.topic(id), [id]);

  return (
    <>
      <p className="crumbs">
        <Link to="/topics">Теми</Link> /
      </p>
      <Async state={state}>
        {(t) => (
          <>
            <h1>
              {t.topic_label} <span className="muted">{t.topic_id}</span>
            </h1>
            <Card>
              <Fields
                items={[
                  ["Опис (meaning)", text(t.meaning)],
                  ["Повʼязані терміни", text(t.related_terms)],
                  ["Синоніми", text(t.synonyms)],
                  ["Як називають клієнти", text(t.client_aliases)],
                  ["Активна", fmtBool(t.is_active)],
                  ["Створено", fmtDate(t.created_at)],
                  ["Оновлено", fmtDate(t.updated_at)],
                ]}
              />
            </Card>

            <div className="grid-2">
              <Card title="Пріоритет теми">
                <PriorityForm key={t.topic_label} initialLabel={t.topic_label} onDone={state.reload} />
              </Card>
              <Card title="Топ-організація теми">
                <TopOrganizationForm key={t.topic_label} initialLabel={t.topic_label} onDone={state.reload} />
              </Card>
            </div>

            <Card title="Оцінки з максимальним балом">
              <p className="small muted">таблична функція MAX_EVALUATION_BY_TOPIC</p>
              <MaxEvaluation topicLabel={t.topic_label} />
            </Card>

            <Card title="Усі оцінки теми">
              <RelatedEvaluations filter={{ canonical_topic_id: id }} hide={["topic"]} />
            </Card>
          </>
        )}
      </Async>
    </>
  );
}

export function MaxEvaluation({ topicLabel }: { topicLabel: string }) {
  const state = useFetch(() => api.maxEvaluationByTopic(topicLabel), [topicLabel]);
  return <Async state={state}>{(d) => <MaxEvaluationTable rows={d.items} />}</Async>;
}

function MaxEvaluationTable({ rows }: { rows: MaxEvaluationRow[] }) {
  // функція повертає один рядок з info, якщо оцінок немає
  const info = rows.find((r) => r.info)?.info;
  if (info) return <p className="muted">{info}</p>;
  return (
    <table>
      <thead>
        <tr>
          <th>Оцінка</th>
          <th>Тікет</th>
          <th>Бал</th>
          <th>Результат</th>
          <th>Створено</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.qa_evaluation_id}>
            <td>
              <Link to={`/evaluations/${r.qa_evaluation_id}`}>{r.qa_evaluation_id}</Link>
            </td>
            <td>
              <Link to={`/tickets/${r.ticket_id}`}>{r.ticket_id}</Link>
            </td>
            <td>{fmtScore(r.overall_score)}</td>
            <td>
              <ResultBadge result={r.result} />
            </td>
            <td>{fmtDate(r.created_at)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
