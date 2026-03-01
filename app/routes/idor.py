"""
Insecure Direct Object Reference (IDOR) lab.

VULNERABILITIES:
  - Predictable, sequential user/resource IDs
  - No authorization checks on resource access
  - Direct database row access via user-supplied ID
"""

from flask import Blueprint, render_template, request, session, flash, jsonify

from app.database import get_db

bp = Blueprint("idor", __name__)


@bp.route("/")
def index():
    return render_template("labs/idor.html")


@bp.route("/profile/<int:user_id>")
def profile(user_id):
    """View any user's profile by changing the ID in the URL."""
    db = get_db()

    # VULN: No authorization check - any user can view any profile
    user = db.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if not user:
        flash("User not found.", "danger")
        return render_template("labs/idor_profile.html", target_user=None)

    return render_template("labs/idor_profile.html", target_user=user)


@bp.route("/orders/<int:order_id>")
def order_detail(order_id):
    """View any order by changing the order ID."""
    db = get_db()

    # VULN: No ownership verification
    order = db.execute(
        "SELECT o.*, u.username, p.name as product_name "
        "FROM orders o "
        "JOIN users u ON o.user_id = u.id "
        "JOIN products p ON o.product_id = p.id "
        "WHERE o.id = ?",
        (order_id,),
    ).fetchone()

    return render_template("labs/idor_order.html", order=order)


@bp.route("/api/messages/<int:message_id>")
def get_message(message_id):
    """API endpoint to retrieve any message - no auth check."""
    db = get_db()

    # VULN: No authentication or authorization
    message = db.execute(
        "SELECT m.*, s.username as sender, r.username as receiver "
        "FROM messages m "
        "JOIN users u AS s ON m.sender_id = s.id "
        "JOIN users u AS r ON m.receiver_id = r.id "
        "WHERE m.id = ?",
        (message_id,),
    ).fetchone()

    if not message:
        return jsonify({"error": "Message not found"}), 404

    return jsonify(dict(message))
