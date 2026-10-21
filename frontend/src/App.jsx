import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';

export default function App() {
  const saved = localStorage.getItem('user');
  const [user, setUser] = useState(saved ? JSON.parse(saved) : null);

  function logout() {
    localStorage.removeItem('user');
    setUser(null);
  }

  if (!user) {
    return <LoginPage onLogin={setUser} />;
  }

  return <MainPage user={user} onLogout={logout} />;
}
