import { useEffect, useState } from "react";
import { api } from "../services/api";

const EMPTY_FORM = { amount: "", description: "", type: "expense", date: new Date().toISOString().split("T")[0], category_id: "" };

function formatCurrency(val) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 }).format(val);
}

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getTransactions(), api.getCategories()])
      .then(([txs, cats]) => { setTransactions(txs); setCategories(cats); })
      .finally(() => setLoading(false));
  }, []);

  const filteredCategories = categories.filter((c) => c.type === form.type);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value, ...(name === "type" ? { category_id: "" } : {}) }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setFormError(null);
    try {
      const newTx = await api.createTransaction({ ...form, amount: parseFloat(form.amount), category_id: parseInt(form.category_id) });
      setTransactions((prev) => [newTx, ...prev]);
      setForm(EMPTY_FORM);
    } catch (err) {
      setFormError(err.message);
    }
  }

  async function handleDelete(id) {
    try {
      await api.deleteTransaction(id);
      setTransactions((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      alert(err.message);
    }
  }

  if (loading) return <p className="loading">Loading...</p>;

  return (
    <div className="page">
      <h1 className="page-title">Transactions</h1>
      <form className="tx-form" onSubmit={handleSubmit}>
        <h2 className="form-title">Add Transaction</h2>
        {formError && <p className="error-msg">{formError}</p>}
        <div className="form-row">
          <label>Type<select name="type" value={form.type} onChange={handleChange}><option value="income">Income</option><option value="expense">Expense</option></select></label>
          <label>Category<select name="category_id" value={form.category_id} onChange={handleChange} required><option value="">Select category</option>{filteredCategories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
        </div>
        <div className="form-row">
          <label>Amount (₹)<input name="amount" type="number" min="0.01" step="0.01" value={form.amount} onChange={handleChange} required placeholder="0.00" /></label>
          <label>Date<input name="date" type="date" value={form.date} max={new Date().toISOString().split("T")[0]} onChange={handleChange} required /></label>
        </div>
        <label>Description<input name="description" type="text" value={form.description} onChange={handleChange} required placeholder="What was this for?" maxLength={200} /></label>
        <button type="submit" className="btn-primary">Add Transaction</button>
      </form>
      <div className="tx-list">
        <h2 className="section-title">History</h2>
        {transactions.length === 0 ? <p className="empty-msg">No transactions yet.</p> : transactions.map((tx) => (
          <div key={tx.id} className={`tx-item tx-${tx.type}`}>
            <div className="tx-left">
              <span className="tx-category">{tx.category.name}</span>
              <span className="tx-desc">{tx.description}</span>
              <span className="tx-date">{tx.date}</span>
            </div>
            <div className="tx-right">
              <span className="tx-amount">{tx.type === "income" ? "+" : "−"}{formatCurrency(tx.amount)}</span>
              <button className="btn-delete" onClick={() => handleDelete(tx.id)} title="Delete">×</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
