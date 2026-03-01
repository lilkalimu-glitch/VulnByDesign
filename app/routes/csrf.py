"""
Cross-Site Request Forgery (CSRF) lab.

VULNERABILITIES:
  - No CSRF tokens on state-changing forms
  - Password change without current password verification
  - Email change without confirmation
"""

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from app.database import get_db

bp = Blueprint("csrf", __name__)


@bp.route("/")
def index():
    return render_template("labs/csrf.html")


@bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    """Change password - no CSRF token, no current password required."""
    if request.method == "POST":
        new_password = request.form.get("new_password", "")
        user = session.get("user")

        if not user:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))

        db = get_db()
        # VULN: No CSRF token, no old password check, plaintext storage
        db.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (new_password, user["id"]),
        )
        db.commit()
        flash("Password changed successfully.", "success")

    return render_template("labs/csrf_password.html")


@bp.route("/change-email", methods=["GET", "POST"])
def change_email():
    """Change email - no CSRF token, no confirmation required."""
    if request.method == "POST":
        new_email = request.form.get("new_email", "")
        user = session.get("user")

        if not user:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))

        db = get_db()
        # VULN: No CSRF token, no email confirmation
        db.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (new_email, user["id"]),
        )
        db.commit()
        flash("Email updated successfully.", "success")

    return render_template("labs/csrf_email.html")


@bp.route("/transfer", methods=["GET", "POST"])
def transfer():
    """Simulate money transfer - no CSRF protection."""
    if request.method == "POST":
        recipient = request.form.get("recipient", "")
        amount = request.form.get("amount", "0")

        # VULN: No CSRF token on financial operation
        flash(f"Transfer of ${amount} to {recipient} completed.", "success")

    return render_template("labs/csrf_transfer.html")
