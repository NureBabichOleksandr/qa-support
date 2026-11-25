import { useState, type FormEvent } from "react";
import { api, type Topic } from "../api";
import { ErrorBox } from "./ui";

/** Спільний стан форми, що викликає процедуру: busy / помилка / результат. */
function useAction() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<Error>();
  const [result, setResult] = useState<Topic>();

  const run = async (fn: () => Promise<Topic>, onDone?: (t: Topic) => void) => {
    setBusy(true);
    setError(undefined);
    setResult(undefined);
    try {
      const topic = await fn();
      setResult(topic);
      onDone?.(topic);
    } catch (e) {
      setError(e as Error);
    } finally {
      setBusy(false);
    }
  };
  return { busy, error, result, run };
}

/** Процедура SET_TOPIC_PRIORITY. Порожня назва → THROW 50001 на сервері. */
export function PriorityForm({ initialLabel = "", onDone }: { initialLabel?: string; onDone?: (t: Topic) => void }) {
  const [label, setLabel] = useState(initialLabel);
  const [percent, setPercent] = useState(50);
  const { busy, error, result, run } = useAction();

  const submit = (e: FormEvent) => {
    e.preventDefault();
    run(() => api.setTopicPriority(label, percent), onDone);
  };

  return (
    <form onSubmit={submit} className="form">
      <label>
        Тема
        <input value={label} onChange={(e) => setLabel(e.target.value)} list="topic-labels" placeholder="Біллінг" />
      </label>
      <label>
        Пріоритет, %
        <input type="number" value={percent} onChange={(e) => setPercent(Number(e.target.value))} />
      </label>
      <button disabled={busy}>Виконати SET_TOPIC_PRIORITY</button>
      {error && <ErrorBox error={error} />}
      {result && (
        <div className="alert alert-ok">
          «{result.topic_label}»: meaning = «{result.meaning}»
        </div>
      )}
    </form>
  );
}

/** Процедура SET_TOP_ORGANIZATION_FOR_TOPIC (код повернення 1 → 404, 2 → 409). */
export function TopOrganizationForm({
  initialLabel = "",
  onDone,
}: {
  initialLabel?: string;
  onDone?: (t: Topic) => void;
}) {
  const [label, setLabel] = useState(initialLabel);
  const { busy, error, result, run } = useAction();

  const submit = (e: FormEvent) => {
    e.preventDefault();
    run(() => api.setTopOrganization(label), onDone);
  };

  return (
    <form onSubmit={submit} className="form">
      <label>
        Тема
        <input value={label} onChange={(e) => setLabel(e.target.value)} list="topic-labels" placeholder="Інтеграції" />
      </label>
      <button disabled={busy}>Виконати SET_TOP_ORGANIZATION_FOR_TOPIC</button>
      {error && <ErrorBox error={error} />}
      {result && (
        <div className="alert alert-ok">
          «{result.topic_label}»: related_terms = «{result.related_terms}»
        </div>
      )}
    </form>
  );
}
