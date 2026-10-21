from datetime import date

from flask import Blueprint, jsonify, request

from database.db import get_db_connection

finance_bp = Blueprint("finance", __name__, url_prefix="/api/finance")


def current_month_range():
    today = date.today()
    start = today.replace(day=1)
    if today.month == 12:
        end = date(today.year + 1, 1, 1)
    else:
        end = date(today.year, today.month + 1, 1)
    return start, end


@finance_bp.get("/summary/<int:uid>")
def summary(uid):
    start, end = current_month_range()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) AS income, "
            "COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS expense "
            "FROM transactions "
            "WHERE user_id=%s AND transaction_date>=%s AND transaction_date<%s",
            (uid, start, end),
        )
        totals = cursor.fetchone()

        cursor.execute(
            "SELECT category, SUM(amount) AS amount "
            "FROM transactions "
            "WHERE user_id=%s AND type='expense' "
            "AND transaction_date>=%s AND transaction_date<%s "
            "GROUP BY category ORDER BY amount DESC",
            (uid, start, end),
        )
        categories = cursor.fetchall()

        cursor.execute(
            "SELECT transaction_id, type, amount, category, transaction_date, note, currency "
            "FROM transactions "
            "WHERE user_id=%s "
            "ORDER BY transaction_date DESC, transaction_id DESC "
            "LIMIT 30",
            (uid,),
        )
        transactions = cursor.fetchall()
        for tx in transactions:
            tx["transaction_date"] = tx["transaction_date"].isoformat()

        cursor.execute(
            "SELECT limit_amount, start_date, end_date "
            "FROM budgets "
            "WHERE user_id=%s AND start_date<=%s AND end_date>=%s "
            "ORDER BY budget_id DESC LIMIT 1",
            (uid, start, end),
        )
        budget = cursor.fetchone()
        if budget:
            budget["limit_amount"] = float(budget["limit_amount"])
            budget["start_date"] = budget["start_date"].isoformat()
            budget["end_date"] = budget["end_date"].isoformat()

        cursor.execute(
            "SELECT target_amount, deadline "
            "FROM savings_goals "
            "WHERE user_id=%s "
            "ORDER BY goal_id DESC LIMIT 1",
            (uid,),
        )
        goal = cursor.fetchone()
        if goal:
            goal["target_amount"] = float(goal["target_amount"])
            goal["deadline"] = goal["deadline"].isoformat() if goal["deadline"] else None

        income = float(totals["income"])
        expense = float(totals["expense"])

        return jsonify(
            income=income,
            expense=expense,
            savings=income - expense,
            categories=categories,
            transactions=transactions,
            budget=budget,
            goal=goal,
        )
    finally:
        cursor.close()
        conn.close()


@finance_bp.post("/transactions")
def add_transaction():
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO transactions"
            "(user_id, type, amount, category, transaction_date, note, currency) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (
                data["user_id"],
                data["type"],
                data["amount"],
                data["category"],
                data["transaction_date"],
                data.get("note"),
                data.get("currency", "INR"),
            ),
        )
        conn.commit()
        return jsonify(success=True), 201
    except Exception as exc:
        conn.rollback()
        print(exc)
        return jsonify(success=False, message="Could not add transaction"), 500
    finally:
        cursor.close()
        conn.close()


@finance_bp.delete("/transactions/<int:tid>")
def delete_transaction(tid):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE transaction_id=%s", (tid,))
        conn.commit()
        return jsonify(success=True)
    finally:
        cursor.close()
        conn.close()


@finance_bp.post("/budget")
def set_budget():
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO budgets(user_id, limit_amount, start_date, end_date) "
            "VALUES(%s, %s, %s, %s)",
            (
                data["user_id"],
                data["limit_amount"],
                data["start_date"],
                data["end_date"],
            ),
        )
        conn.commit()
        return jsonify(success=True), 201
    finally:
        cursor.close()
        conn.close()


@finance_bp.post("/goal")
def set_goal():
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO savings_goals(user_id, target_amount, deadline) "
            "VALUES(%s, %s, %s)",
            (data["user_id"], data["target_amount"], data.get("deadline")),
        )
        conn.commit()
        return jsonify(success=True), 201
    finally:
        cursor.close()
        conn.close()
