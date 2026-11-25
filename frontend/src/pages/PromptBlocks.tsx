import { api } from "../api";
import { Async, Card, Pagination } from "../components/ui";
import { fmtDate, text } from "../format";
import { useFetch, useQueryState } from "../hooks";

export function PromptBlocksPage() {
  const q = useQueryState();
  const state = useFetch(() => api.promptBlocks({ page: q.page }), [q.page]);

  return (
    <>
      <h1>Блоки промпту</h1>
      <Card>
        <Async state={state}>
          {(page) => (
            <>
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Текст</th>
                    <th>Версія</th>
                    <th>Автор</th>
                    <th>Створено</th>
                  </tr>
                </thead>
                <tbody>
                  {page.items.map((b) => (
                    <tr key={b.prompt_block_id}>
                      <td>{b.prompt_block_id}</td>
                      <td>{text(b.text)}</td>
                      <td>{text(b.version)}</td>
                      <td>{text(b.added_by)}</td>
                      <td>{fmtDate(b.created_at)}</td>
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
