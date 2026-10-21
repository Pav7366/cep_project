# Financial Manager

A personal + group finance tracker.

## Tech stack

| Layer | Technologies |
|---|---|
| Login page | React + Vite + JavaScript + CSS |
| Main page | React + Vite + JavaScript + CSS |
| Backend | Python + Flask |
| Database | MySQL |
| Communication | HTTP/JSON + Fetch API |

## Project structure

```
financial-manager/
├── frontend/                  # React + Vite (JavaScript + CSS)
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx           # Entry point
│       ├── App.jsx            # Chooses Login page or Main page
│       ├── styles.css         # Global styles
│       ├── services/api.js    # Fetch API wrapper (HTTP/JSON)
│       ├── pages/
│       │   ├── LoginPage.jsx / LoginPage.css    # Login page
│       │   └── MainPage.jsx / MainPage.css      # Main page
│       └── components/
│           ├── PersonalTab.jsx                  # Personal finance tab
│           ├── GroupsTab.jsx                    # Splitwise tab
│           └── ToolsTab.jsx                     # EMI calculator tab
└── backend/                   # Python + Flask
    ├── app.py                 # Flask entry point (port 5000)
    ├── config.py              # Loads .env config
    ├── requirements.txt
    ├── .env / .env.example    # MySQL credentials
    ├── database/
    │   ├── db.py              # MySQL connection helper
    │   └── schema.sql         # MySQL schema
    └── routes/
        ├── auth.py            # Register / login / forgot-password
        ├── finance.py         # Summary, transactions, budget, goal
        ├── groups.py          # Groups, members, expenses, balances
        └── tools.py           # EMI + currency calculators
```

## Run the database

1. Install MySQL.
2. Create the database and tables:
   ```
   mysql -u root -p < backend/database/schema.sql
   ```

## Run the backend (Python + Flask)

1. Install Python 3.11+.
2. Copy `backend/.env.example` to `backend/.env` and set `DB_PASSWORD`.
3. ```
   cd backend
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python app.py`

Backend API: http://localhost:5000

## Run the frontend (React + Vite)

1. Install Node.js LTS.
2. ```
   cd frontend
   npm install
   npm run dev
   ```

Frontend: http://localhost:5173

The frontend talks to the backend over HTTP with JSON payloads using the Fetch API (`frontend/src/services/api.js`).

## Features

- Registration / login / logout
- Personal dashboard: monthly income, expense and savings totals
- Add transactions (income or expense) with category, date and note
- Expense breakdown by category for the current month
- Latest 30 transactions
- Groups (Splitwise): create groups, view members, per-member paid/owed/net balances, group expenses
- EMI calculator

No JWT/session authentication yet. Advanced features are future scope.
