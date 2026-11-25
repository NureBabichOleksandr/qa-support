import type { ReactNode } from "react";
import { ApiError } from "../api";

/** Показує помилку. Користувацький виняток з БД (THROW 5xxxx) виділено окремо. */
export function ErrorBox({ error }: { error: Error }) {
  if (error instanceof ApiError && error.isDatabaseError) {
    return (
      <div className="alert alert-db">
        <strong>Виняток СУБД #{error.errorNumber}</strong>
        <div>{error.message}</div>
      </div>
    );
  }
  const status = error instanceof ApiError ? `HTTP ${error.status}: ` : "";
  return (
    <div className="alert alert-error">
      {status}
      {error.message}
    </div>
  );
}

export function Async<T>({
  state,
  children,
}: {
  state: { data?: T; error?: Error; loading: boolean };
  children: (data: T) => ReactNode;
}) {
  if (state.error) return <ErrorBox error={state.error} />;
  if (state.data === undefined) return <p className="muted">Завантаження…</p>;
  return <div style={{ opacity: state.loading ? 0.5 : 1 }}>{children(state.data)}</div>;
}

export function Pagination({
  page,
  totalPages,
  total,
  onChange,
}: {
  page: number;
  totalPages: number;
  total: number;
  onChange: (page: number) => void;
}) {
  return (
    <div className="pagination">
      <button disabled={page <= 1} onClick={() => onChange(page - 1)}>
        ←
      </button>
      <span>
        {page} / {totalPages} <span className="muted">(усього {total})</span>
      </span>
      <button disabled={page >= totalPages} onClick={() => onChange(page + 1)}>
        →
      </button>
    </div>
  );
}

/** Сітка «назва — значення» для картки запису. */
export function Fields({ items }: { items: [string, ReactNode][] }) {
  return (
    <dl className="fields">
      {items.map(([label, value]) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

/** Текстовий фільтр: застосовується по Enter або при втраті фокусу. */
export function FilterInput({
  value,
  placeholder,
  onApply,
}: {
  value: string;
  placeholder: string;
  onApply: (value: string) => void;
}) {
  return (
    <input
      key={value}
      placeholder={placeholder}
      defaultValue={value}
      onBlur={(e) => e.target.value !== value && onApply(e.target.value.trim())}
      onKeyDown={(e) => e.key === "Enter" && e.currentTarget.blur()}
    />
  );
}

export function ResultBadge({ result }: { result: string | null }) {
  if (!result) return <span className="muted">—</span>;
  return <span className={`badge badge-${result}`}>{result}</span>;
}

export function Card({ title, children }: { title?: ReactNode; children: ReactNode }) {
  return (
    <section className="card">
      {title && <h2>{title}</h2>}
      {children}
    </section>
  );
}
