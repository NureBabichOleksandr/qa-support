import { useState, type FormEvent } from "react";
import { api } from "../api";
import { PriorityForm, TopOrganizationForm } from "../components/TopicForms";
import { Async, Card } from "../components/ui";
import { useFetch } from "../hooks";
import { MaxEvaluation } from "./Topics";

/** Усі підпрограми БД на одній сторінці — для демонстрації пунктів 2–4 ЛР3. */
export function RoutinesPage() {
  return (
    <>
      <h1>Процедури й функції</h1>

      <div className="grid-2">
        <Card title="SET_TOPIC_PRIORITY">
          <p className="small muted">
            Процедура записує пріоритет у meaning теми. Залиште назву порожньою або з пробілом — сервер БД кине
            користувацький виняток <code>THROW 50001</code>.
          </p>
          <PriorityForm />
        </Card>
        <Card title="SET_TOP_ORGANIZATION_FOR_TOPIC">
          <p className="small muted">
            Процедура записує в related_terms організацію з найбільшою кількістю тікетів за темою.
          </p>
          <TopOrganizationForm />
        </Card>
      </div>

      <div className="grid-2">
        <Card title="req_count_by_agnet_NAME · TOP_TOPIC_BY_AGENT_NAME">
          <p className="small muted">Скалярна функція (кількість оцінених тікетів) і таблична (найчастіші теми).</p>
          <AgentFunctions />
        </Card>
        <Card title="MAX_EVALUATION_BY_TOPIC">
          <p className="small muted">Таблична функція: оцінки з максимальним балом за темою.</p>
          <TopicFunction />
        </Card>
      </div>
    </>
  );
}

function AgentFunctions() {
  const agents = useFetch(api.agents, []);
  const [agent, setAgent] = useState("");
  const count = useFetch(async () => (agent ? api.evaluatedTicketsCount(agent) : null), [agent]);
  const top = useFetch(async () => (agent ? api.topTopicsByAgent(agent) : null), [agent]);

  return (
    <div className="form">
      <label>
        Агент
        <select value={agent} onChange={(e) => setAgent(e.target.value)}>
          <option value="">— оберіть —</option>
          {agents.data?.map((a) => <option key={a}>{a}</option>)}
        </select>
      </label>
      {agent && (
        <>
          <Async state={count}>
            {(d) => (
              <p>
                Оцінених тікетів: <strong>{d?.evaluated_tickets}</strong>
              </p>
            )}
          </Async>
          <Async state={top}>
            {(d) => (
              <ul className="chips">
                {d?.topic_labels.map((l) => <li key={l}>{l}</li>)}
              </ul>
            )}
          </Async>
        </>
      )}
    </div>
  );
}

function TopicFunction() {
  const [input, setInput] = useState("");
  const [label, setLabel] = useState("");

  const submit = (e: FormEvent) => {
    e.preventDefault();
    setLabel(input.trim());
  };

  return (
    <>
      <form onSubmit={submit} className="form">
        <label>
          Тема
          <input value={input} onChange={(e) => setInput(e.target.value)} list="topic-labels" placeholder="Біллінг" />
        </label>
        <button disabled={!input.trim()}>Виконати</button>
      </form>
      {label && <MaxEvaluation topicLabel={label} />}
    </>
  );
}
