"""
Cross-Site Scripting (XSS) lab.

VULNERABILITIES:
  - Reflected XSS (unsanitized query parameters rendered in page)
  - Stored XSS (user-submitted content rendered without escaping)
  - DOM-based XSS (client-side JS uses location.hash unsafely)
"""

from flask import Blueprint, render_template, request, Markup

from app.database import get_db

bp = Blueprint("xss", __name__)


@bp.route("/")
def index():
    return render_template("labs/xss.html")


@bp.route("/reflected")
def reflected():
    """Reflected XSS - search query echoed back without escaping."""
    query = request.args.get("q", "")

    # VULN: Rendering user input without escaping via Markup()
    safe_query = Markup(query) if query else ""

    return render_template("labs/xss_reflected.html", query=safe_query)


@bp.route("/stored", methods=["GET", "POST"])
def stored():
    """Stored XSS - comments stored and rendered without sanitization."""
    db = get_db()

    if request.method == "POST":
        title = request.form.get("title", "")
        body = request.form.get("body", "")
        user = {"id": 1}  # Simulated logged-in user

        db.execute(
            "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)",
            (user["id"], title, body),
        )
        db.commit()

    posts = db.execute(
        "SELECT id, title, body, created_at FROM posts ORDER BY created_at DESC"
    ).fetchall()

    return render_template("labs/xss_stored.html", posts=posts)


@bp.route("/dom")
def dom_based():
    """DOM-based XSS - client-side rendering from URL fragment."""
    return render_template("labs/xss_dom.html")
