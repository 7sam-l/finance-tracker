import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import "./index.css";

const NAV = [
  { key: "dashboard", label: "Dashboard" },
  { key: "transactions", label: "Transactions" },
];

export default function App() {
  const [page, setPage] = useState("dashboard");
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-icon">₹</span>
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
      </main>
    </div>
  );
}
