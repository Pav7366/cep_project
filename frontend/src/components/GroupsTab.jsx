import { useEffect, useState } from 'react';
import { api } from '../services/api';

const GROUP_TYPES = ['TRIP', 'PROJECT', 'FUNCTION', 'FESTIVAL', 'OTHER'];

export default function GroupsTab({ user }) {
  const [groups, setGroups] = useState([]);
  const [detail, setDetail] = useState(null);
  const [name, setName] = useState('');
  const [type, setType] = useState('TRIP');
  const [error, setError] = useState('');

  async function loadGroups() {
    try {
      const result = await api.getGroups(user.user_id);
      setGroups(result.groups);
      setError('');
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    loadGroups();
  }, []);

  async function createGroup(event) {
    event.preventDefault();
    try {
      await api.createGroup({
        owner_id: user.user_id,
        name,
        group_type: type
      });
      setName('');
      loadGroups();
    } catch (e) {
      setError(e.message);
    }
  }

  async function openGroup(groupId) {
    try {
      setDetail(await api.getGroup(groupId));
      setError('');
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <main className="container">
      {error && <p className="error">{error}</p>}

      <div className="grid">
        <section className="card">
          <h2>Create Group</h2>
          <form className="compact" onSubmit={createGroup}>
            <input
              placeholder="Group name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <select value={type} onChange={(e) => setType(e.target.value)}>
              {GROUP_TYPES.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
            <button>Create</button>
          </form>
        </section>

        <section className="card">
          <h2>Your Groups</h2>
          {groups.map((g) => (
            <button
              className="group"
              key={g.group_id}
              onClick={() => openGroup(g.group_id)}
            >
              {g.name}
              <span>{g.group_type}</span>
            </button>
          ))}
        </section>
      </div>

      {detail && (
        <section className="card">
          <h2>Members</h2>
          <div className="chips">
            {detail.members.map((m) => (
              <label key={m.user_id}>{m.name}</label>
            ))}
          </div>

          <h2>Balances</h2>
          <div className="table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Paid</th>
                  <th>Owed</th>
                  <th>Net</th>
                </tr>
              </thead>
              <tbody>
                {detail.balances.map((b) => (
                  <tr key={b.user_id}>
                    <td>{b.name}</td>
                    <td>₹{Number(b.paid).toFixed(2)}</td>
                    <td>₹{Number(b.owed).toFixed(2)}</td>
                    <td>₹{Number(b.balance).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h2>Expenses</h2>
          {detail.expenses.map((e) => (
            <p key={e.expense_id}>
              {e.payer} paid ₹{Number(e.amount).toFixed(2)} for {e.category}
            </p>
          ))}
        </section>
      )}
    </main>
  );
}
