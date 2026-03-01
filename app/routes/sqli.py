"""
SQL Injection lab.

VULNERABILITIES:
  - Classic SQL injection via string concatenation
  - Union-based injection
  - Blind SQL injection
"""

from flask import Blueprint, render_template, request

from app.database import get_db

bp = Blueprint("sqli", __name__)


@bp.route("/")
def index():
    return render_template("labs/sqli.html")


@bp.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query_used = ""
    error = None

    search_term = request.args.get("q", "") or request.form.get("q", "")

    if search_term:
        db = get_db()

        # VULN: SQL Injection via string concatenation
        query = f"SELECT id, name, description, price FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        query_used = query

        try:
            results = db.execute(query).fetchall()
        except Exception as e:
            error = str(e)

    return render_template(
        "labs/sqli.html",
        results=results,
        search_term=search_term,
        query_used=query_used,
        error=error,
    )


@bp.route("/user-lookup", methods=["GET", "POST"])
def user_lookup():
    """Lookup user profile by ID - vulnerable to blind SQL injection."""
    user = None
    error = None
    user_id = request.args.get("id", "") or request.form.get("id", "")

    if user_id:
        db = get_db()

        # VULN: Blind SQL Injection
        query = f"SELECT id, username, email, role FROM users WHERE id = {user_id}"

        try:
            user = db.execute(query).fetchone()
        except Exception as e:
            error = str(e)

    return render_template(
        "labs/sqli_user_lookup.html",
        user=user,
        user_id=user_id,
        error=error,
    )
