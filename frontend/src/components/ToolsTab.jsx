import { useState } from 'react';
import { api } from '../services/api';

export default function ToolsTab() {
  const [form, setForm] = useState({
    principal: '',
    annual_rate: '',
    months: ''
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  function update(field, value) {
    setForm({ ...form, [field]: value });
  }

  async function calculate(event) {
    event.preventDefault();
    try {
      setResult(await api.calculateEmi(form));
      setError('');
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <main className="container">
      <section className="card">
        <h2>EMI Calculator</h2>
        <form className="compact" onSubmit={calculate}>
          <input
            placeholder="Principal"
            value={form.principal}
            onChange={(e) => update('principal', e.target.value)}
            required
          />
          <input
            placeholder="Annual rate %"
            value={form.annual_rate}
            onChange={(e) => update('annual_rate', e.target.value)}
            required
          />
          <input
            placeholder="Months"
            value={form.months}
            onChange={(e) => update('months', e.target.value)}
            required
          />
          <button>Calculate</button>
        </form>

        {error && <p className="error">{error}</p>}

        {result && (
          <p>
            Monthly EMI: <b>₹{result.monthly_emi}</b>
            <br />
            Interest: ₹{result.total_interest}
          </p>
        )}
      </section>
    </main>
  );
}
