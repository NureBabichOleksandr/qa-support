import { NavLink, Outlet } from "react-router";
import { api } from "../api";
import { useFetch } from "../hooks";

const links = [
  ["/agents", "Агенти"],
  ["/evaluations", "Оцінки"],
  ["/tickets", "Тікети"],
  ["/topics", "Теми"],
  ["/prompt-blocks", "Блоки промпту"],
  ["/routines", "Процедури й функції"],
] as const;

export function Layout() {
  const health = useFetch(api.health, []);
  const ok = health.data?.status === "ok";
  // підказки назв тем для форм процедур
  const topics = useFetch(() => api.topics({ limit: 100 }), []);

  return (
    <div className="layout">
      <aside>
        <div className="logo">QA Support</div>
        <nav>
          {links.map(([to, label]) => (
            <NavLink key={to} to={to}>
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="health" title={health.error?.message}>
          <span className={`dot ${health.loading ? "" : ok ? "dot-ok" : "dot-bad"}`} />
          {health.loading ? "перевірка…" : ok ? `API · БД ${health.data?.database}` : "API недоступне"}
        </div>
      </aside>
      <main>
        <Outlet />
      </main>
      <datalist id="topic-labels">
        {topics.data?.items.map((t) => <option key={t.canonical_topic_id} value={t.topic_label} />)}
      </datalist>
    </div>
  );
}
