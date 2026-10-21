from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not all([name, mobile, email, password]):
        return jsonify(success=False, message="All fields are required"), 400
    if len(password) < 8:
        return jsonify(
            success=False, message="Password must contain at least 8 characters"
        ), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM users WHERE email=%s OR mobile=%s",
            (email, mobile),
        )
        if cursor.fetchone():
            return jsonify(
                success=False, message="Email or mobile already registered"
            ), 409

        cursor.execute(
            "INSERT INTO users(name, mobile, email, password_hash) "
            "VALUES(%s, %s, %s, %s)",
            (name, mobile, email, generate_password_hash(password)),
        )
        conn.commit()
        return jsonify(success=True, message="Registration successful"), 201
    except Exception as exc:
        conn.rollback()
        print(exc)
        return jsonify(success=False, message="Registration failed"), 500
    finally:
        cursor.close()
        conn.close()


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify(success=False, message="Email and password are required"), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT user_id, name, mobile, email, password_hash "
            "FROM users WHERE email=%s",
            (email,),
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify(success=False, message="Invalid email or password"), 401

        user.pop("password_hash")
        return jsonify(success=True, message="Login successful", user=user)
    finally:
        cursor.close()
        conn.close()


@auth_bp.post("/forgot-password")
def forgot_password():
    return jsonify(
        success=True,
        message="Password reset email will be added in a later phase.",
    )
