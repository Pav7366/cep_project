import { useState } from 'react';
import { api } from '../services/api';
import './LoginPage.css';

export default function LoginPage({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({
    name: '',
    mobile: '',
    email: '',
    password: ''
  });
  const [message, setMessage] = useState('');

  function update(field, value) {
    setForm({ ...form, [field]: value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage('');

    try {
      let result;

      if (mode === 'login') {
        result = await api.login({ email: form.email, password: form.password });
      } else if (mode === 'register') {
        result = await api.register(form);
      } else {
        result = await api.forgotPassword(form.email);
      }

      setMessage(result.message);

      if (result.user) {
        localStorage.setItem('user', JSON.stringify(result.user));
        onLogin(result.user);
      }
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <main className="auth">
      <section className="card">
        <h1>
          {mode === 'login' && 'Welcome Back'}
          {mode === 'register' && 'Create Account'}
          {mode === 'forgot' && 'Reset Password'}
        </h1>

        <form onSubmit={handleSubmit}>
          {mode === 'register' && (
            <>
              <label>
                Name
                <input
                  value={form.name}
                  onChange={(e) => update('name', e.target.value)}
                  required
                />
              </label>
              <label>
                Mobile
                <input
                  value={form.mobile}
                  onChange={(e) => update('mobile', e.target.value)}
                  pattern="[0-9]{10}"
                  required
                />
              </label>
            </>
          )}

          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={(e) => update('email', e.target.value)}
              required
            />
          </label>

          {mode !== 'forgot' && (
            <label>
              Password
              <input
                type="password"
                value={form.password}
                onChange={(e) => update('password', e.target.value)}
                required
              />
            </label>
          )}

          <button>
            {mode === 'login' && 'Login'}
            {mode === 'register' && 'Create Account'}
            {mode === 'forgot' && 'Request Reset'}
          </button>
        </form>

        {message && <p className="notice">{message}</p>}

        {mode === 'login' ? (
          <>
            <button className="link" onClick={() => setMode('forgot')}>
              Forgot Password?
            </button>
            <button className="secondary" onClick={() => setMode('register')}>
              Create Account
            </button>
          </>
        ) : (
          <button className="secondary" onClick={() => setMode('login')}>
            Back to Login
          </button>
        )}
      </section>
    </main>
  );
}
