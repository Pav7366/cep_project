import { useState } from 'react';
import PersonalTab from '../components/PersonalTab';
import GroupsTab from '../components/GroupsTab';
import ToolsTab from '../components/ToolsTab';
import './MainPage.css';

const TABS = [
  { id: 'personal', label: 'Personal' },
  { id: 'groups', label: 'Splitwise' },
  { id: 'tools', label: 'Tools' }
];

export default function MainPage({ user, onLogout }) {
  const [tab, setTab] = useState('personal');

  return (
    <div className="app">
      <header>
        <b>Financial Manager</b>
        <span>
          Hi, {user.name} <button onClick={onLogout}>Logout</button>
        </span>
      </header>

      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={tab === t.id ? 'active' : ''}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {tab === 'personal' && <PersonalTab user={user} />}
      {tab === 'groups' && <GroupsTab user={user} />}
      {tab === 'tools' && <ToolsTab />}
    </div>
  );
}
