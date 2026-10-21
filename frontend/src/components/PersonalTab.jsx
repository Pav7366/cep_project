import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function PersonalTab({ user }) {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    type: 'expense',
    amount: '',
    category: 'Food',
    transaction_date: new Date().toISOString().slice(0, 10),
    note: ''
  });

  function update(field, value) {
    setForm({ ...form, [field]: value });
  }

  async function loadSummary() {
    try {
      setSummary(await api.getSummary(user.user_id));
      setError('');
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    loadSummary();
  }, []);

  async function addTransaction(event) {
    event.preventDefault();
    try {
      await api.addTransaction({ ...form, user_id: user.user_id });
      setForm({ ...form, amount: '', note: '' });
      loadSummary();
    } catch (e) {
      setError(e.message);
    }
  }

  if (!summary) {
    return <main className="container">{error || 'Loading...'}</main>;
  }

  return (
    <main className="container">
      <div className="stats">
        <div className="stat">
          <span>Income</span>
          <strong>₹{Number(summary.income).toFixed(2)}</strong>
        </div>
        <div className="stat">
          <span>Expense</span>
          <strong>₹{Number(summary.expense).toFixed(2)}</strong>
        </div>
        <div className="stat">
          <span>Savings</span>
          <strong>₹{Number(summary.savings).toFixed(2)}</strong>
        </div>
      </div>

      <div className="grid">
        <section className="card">
          <h2>Add Transaction</h2>
          <form className="compact" onSubmit={addTransaction}>
            <select value={form.type} onChange={(e) => update('type', e.target.value)}>
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
            <input
              type="number"
              placeholder="Amount"
              value={form.amount}
              onChange={(e) => update('amount', e.target.value)}
              required
            />
            <input
              placeholder="Category"
              value={form.category}
              onChange={(e) => update('category', e.target.value)}
            />
            <input
              type="date"
              value={form.transaction_date}
              onChange={(e) => update('transaction_date', e.target.value)}
            />
            <input
              placeholder="Note"
              value={form.note}
              onChange={(e) => update('note', e.target.value)}
            />
            <button>Add</button>
          </form>
        </section>

        <section className="card">
          <h2>Spending Categories</h2>
          {summary.categories.map((c) => (
            <p key={c.category}>
              {c.category}: ₹{Number(c.amount).toFixed(2)}
            </p>
          ))}
        </section>
      </div>

      <section className="card">
        <h2>Transactions</h2>
        {error && <p className="error">{error}</p>}
        <div className="table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Category</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {summary.transactions.map((t) => (
                <tr key={t.transaction_id}>
                  <td>{t.transaction_date}</td>
                  <td>{t.type}</td>
                  <td>{t.category}</td>
                  <td>₹{Number(t.amount).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
