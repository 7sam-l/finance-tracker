import { useEffect, useState } from "react";
import { api } from "../services/api";

function formatCurrency(val) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 }).format(val);
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.getSummary().then(setSummary).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="error-msg">{error}</p>;
  if (!summary) return <p className="loading">Loading...</p>;

  const incomeBreakdown = summary.breakdown.filter((b) => b.type === "income");
  const expenseBreakdown = summary.breakdown.filter((b) => b.type === "expense");

  return (
    <div className="page">
      <h1 className="page-title">Overview</h1>
      <div className="stat-grid">
        <div className={`stat-card stat-${summary.balance >= 0 ? "positive" : "negative"}`}>
          <p className="stat-label">Balance</p>
          <p className="stat-value">{formatCurrency(summary.balance)}</p>
        </div>
        <div className="stat-card stat-positive">
          <p className="stat-label">Total Income</p>
          <p className="stat-value">{formatCurrency(summary.total_income)}</p>
        </div>
        <div className="stat-card stat-negative">
          <p className="stat-label">Total Expenses</p>
          <p className="stat-value">{formatCurrency(summary.total_expenses)}</p>
        </div>
      </div>
      <div className="breakdown-grid">
        {[["Income by Category", incomeBreakdown], ["Expenses by Category", expenseBreakdown]].map(([title, rows]) => (
          <div key={title} className="breakdown-card">
            <h2 className="breakdown-title">{title}</h2>
            {rows.length === 0 ? <p className="empty-msg">No data yet.</p> : (
              <ul className="breakdown-list">
                {rows.map((r, i) => (
                  <li key={i} className="breakdown-row"><span>{r.category}</span><span>{formatCurrency(r.total)}</span></li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
