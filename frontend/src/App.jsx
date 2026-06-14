import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Insights from "./pages/Insights";
import "./index.css";

const NAV = [
  { key: "dashboard", label: "Dashboard" },
  { key: "transactions", label: "Transactions" },
  { key: "insights", label: "Insights" },
];

export default function App() {
  const [page, setPage] = useState("dashboard");
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <img src="/favicon.png" alt="Fintrack Logo" style={{ width: '36px', height: '36px', borderRadius: '8px', objectFit: 'contain' }} />
          <span className="brand-name">Fintrack</span>
        </div>
        <nav className="sidebar-nav">
          {NAV.map((n) => (
            <button key={n.key} className={`nav-item ${page === n.key ? "active" : ""}`} onClick={() => setPage(n.key)}>
              {n.label}
            </button>
          ))}
        </nav>
      </aside>
      <main className="main-content">
        {page === "dashboard" && <Dashboard />}
        {page === "transactions" && <Transactions />}
        {page === "insights" && <Insights />}
      </main>
    </div>
  );
}
