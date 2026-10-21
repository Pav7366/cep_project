const BASE_URL = 'http://localhost:5000/api';

async function request(path, options = {}) {
  const response = await fetch(BASE_URL + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Request failed');
  }

  return data;
}

function post(path, body) {
  return request(path, {
    method: 'POST',
    body: JSON.stringify(body)
  });
}

export const api = {
  register: (data) => post('/auth/register', data),
  login: (data) => post('/auth/login', data),
  forgotPassword: (email) => post('/auth/forgot-password', { email }),

  getSummary: (userId) => request(`/finance/summary/${userId}`),
  addTransaction: (data) => post('/finance/transactions', data),
  deleteTransaction: (transactionId) =>
    request(`/finance/transactions/${transactionId}`, { method: 'DELETE' }),
  setBudget: (data) => post('/finance/budget', data),
  setGoal: (data) => post('/finance/goal', data),

  getGroups: (userId) => request(`/groups/user/${userId}`),
  createGroup: (data) => post('/groups', data),
  getGroup: (groupId) => request(`/groups/${groupId}`),
  addGroupMember: (groupId, data) => post(`/groups/${groupId}/members`, data),
  addGroupExpense: (groupId, data) => post(`/groups/${groupId}/expenses`, data),

  calculateEmi: (data) => post('/tools/emi', data),
  convertCurrency: (data) => post('/tools/currency', data)
};
