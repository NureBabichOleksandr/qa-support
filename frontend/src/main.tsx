import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import { Layout } from "./components/Layout";
import { AgentPage, AgentsPage } from "./pages/Agents";
import { EvaluationPage, EvaluationsPage } from "./pages/Evaluations";
import { PromptBlocksPage } from "./pages/PromptBlocks";
import { RoutinesPage } from "./pages/Routines";
import { TicketPage, TicketsPage } from "./pages/Tickets";
import { TopicPage, TopicsPage } from "./pages/Topics";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Navigate to="/agents" replace />} />
          <Route path="agents" element={<AgentsPage />} />
          <Route path="agents/:name" element={<AgentPage />} />
          <Route path="evaluations" element={<EvaluationsPage />} />
          <Route path="evaluations/:id" element={<EvaluationPage />} />
          <Route path="tickets" element={<TicketsPage />} />
          <Route path="tickets/:id" element={<TicketPage />} />
          <Route path="topics" element={<TopicsPage />} />
          <Route path="topics/:id" element={<TopicPage />} />
          <Route path="prompt-blocks" element={<PromptBlocksPage />} />
          <Route path="routines" element={<RoutinesPage />} />
          <Route path="*" element={<h1>Сторінку не знайдено</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
