"""
Authentication routes.

VULNERABILITIES:
  - Plaintext password storage (no hashing)
  - SQL injection in login
  - No rate limiting
  - Session fixation
  - Verbose error messages (user enumeration)
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from app.database import get_db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()

        # VULN: SQL Injection - string formatting instead of parameterized query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            user = db.execute(query).fetchone()
        except Exception as e:
            # VULN: Verbose error message leaks internal details
            flash(f"Database error: {e}", "danger")
            return render_template("auth/login.html")

        if user:
            # VULN: No session regeneration (session fixation)
            session["user"] = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            }
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("main.index"))
        else:
            # VULN: Reveals whether username exists
            check_user = db.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if check_user:
                flash("Incorrect password for this user.", "danger")
            else:
                flash("No account found with that username.", "danger")

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")

        db = get_db()

        # VULN: No password complexity requirements
        # VULN: Plaintext password storage
        try:
            db.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email),
            )
            db.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Registration failed: {e}", "danger")

    return render_template("auth/register.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
