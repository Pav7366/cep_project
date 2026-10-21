from flask import Blueprint, jsonify, request

from database.db import get_db_connection

groups_bp = Blueprint("groups", __name__, url_prefix="/api/groups")


@groups_bp.get("/user/<int:uid>")
def list_groups(uid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT g.group_id, g.name, g.group_type, COUNT(gm2.user_id) AS member_count "
            "FROM groups_table g "
            "JOIN group_members gm ON gm.group_id = g.group_id "
            "JOIN group_members gm2 ON gm2.group_id = g.group_id "
            "WHERE gm.user_id=%s "
            "GROUP BY g.group_id, g.name, g.group_type "
            "ORDER BY g.group_id DESC",
            (uid,),
        )
        groups = cursor.fetchall()
        return jsonify(groups=groups)
    finally:
        cursor.close()
        conn.close()


@groups_bp.post("")
def create_group():
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO groups_table(owner_id, name, group_type) VALUES(%s, %s, %s)",
            (data["owner_id"], data["name"], data.get("group_type", "OTHER")),
        )
        group_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO group_members(group_id, user_id) VALUES(%s, %s)",
            (group_id, data["owner_id"]),
        )
        conn.commit()
        return jsonify(success=True, group_id=group_id), 201
    finally:
        cursor.close()
        conn.close()


@groups_bp.post("/<int:gid>/members")
def add_member(gid):
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify(success=False, message="User not found"), 404

        cursor.execute(
            "INSERT IGNORE INTO group_members(group_id, user_id) VALUES(%s, %s)",
            (gid, user[0]),
        )
        conn.commit()
        return jsonify(success=True)
    finally:
        cursor.close()
        conn.close()


@groups_bp.get("/<int:gid>")
def group_detail(gid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT u.user_id, u.name, u.email "
            "FROM group_members gm "
            "JOIN users u ON u.user_id = gm.user_id "
            "WHERE gm.group_id=%s",
            (gid,),
        )
        members = cursor.fetchall()

        cursor.execute(
            "SELECT ge.expense_id, ge.amount, ge.category, ge.expense_date, u.name AS payer "
            "FROM group_expenses ge "
            "JOIN users u ON u.user_id = ge.payer_id "
            "WHERE ge.group_id=%s "
            "ORDER BY ge.expense_id DESC",
            (gid,),
        )
        expenses = cursor.fetchall()
        for expense in expenses:
            expense["expense_date"] = expense["expense_date"].isoformat()

        cursor.execute(
            "SELECT u.user_id, u.name, "
            "COALESCE((SELECT SUM(amount) FROM group_expenses "
            "          WHERE group_id=%s AND payer_id=u.user_id), 0) AS paid, "
            "COALESCE(SUM(es.owed_amount), 0) AS owed "
            "FROM users u "
            "JOIN group_members gm ON gm.user_id = u.user_id "
            "LEFT JOIN expense_splits es ON es.user_id = u.user_id "
            "LEFT JOIN group_expenses ge "
            "  ON ge.expense_id = es.expense_id AND ge.group_id=%s "
            "WHERE gm.group_id=%s "
            "GROUP BY u.user_id, u.name",
            (gid, gid, gid),
        )
        balances = cursor.fetchall()
        for balance in balances:
            balance["paid"] = float(balance["paid"])
            balance["owed"] = float(balance["owed"])
            balance["balance"] = round(balance["paid"] - balance["owed"], 2)

        return jsonify(members=members, expenses=expenses, balances=balances)
    finally:
        cursor.close()
        conn.close()


@groups_bp.post("/<int:gid>/expenses")
def add_expense(gid):
    data = request.get_json() or {}
    participants = data.get("participants", [])
    amount = float(data["amount"])

    if not participants:
        return jsonify(success=False, message="Select participants"), 400

    if data.get("split_type", "equal") == "equal":
        share = round(amount / len(participants), 2)
        splits = [(int(p["user_id"]), share) for p in participants]
        last_uid, last_share = splits[-1]
        splits[-1] = (last_uid, round(last_share + amount - sum(s for _, s in splits), 2))
    else:
        splits = [(int(p["user_id"]), float(p["amount"])) for p in participants]
        if round(sum(s for _, s in splits), 2) != round(amount, 2):
            return jsonify(success=False, message="Custom shares must equal total"), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO group_expenses"
            "(group_id, payer_id, amount, category, expense_date, note, currency) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (
                gid,
                data["payer_id"],
                amount,
                data["category"],
                data["expense_date"],
                data.get("note"),
                data.get("currency", "INR"),
            ),
        )
        expense_id = cursor.lastrowid

        for user_id, owed in splits:
            cursor.execute(
                "INSERT INTO expense_splits(expense_id, user_id, owed_amount) "
                "VALUES(%s, %s, %s)",
                (expense_id, user_id, owed),
            )

        conn.commit()
        return jsonify(success=True), 201
    finally:
        cursor.close()
        conn.close()
