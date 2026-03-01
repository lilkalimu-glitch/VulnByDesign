"""Main routes - dashboard and navigation."""

from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint("main", __name__)

VULNERABILITY_LABS = [
    {
        "id": "sqli",
        "name": "SQL Injection",
        "icon": "database",
        "severity": "critical",
        "owasp": "A03:2021 - Injection",
        "description": "Extract data, bypass authentication, or manipulate queries via unsanitized input.",
        "url": "/vuln/sqli/",
    },
    {
        "id": "xss",
        "name": "Cross-Site Scripting (XSS)",
        "icon": "code",
        "severity": "high",
        "owasp": "A03:2021 - Injection",
        "description": "Inject malicious scripts into pages viewed by other users.",
        "url": "/vuln/xss/",
    },
    {
        "id": "csrf",
        "name": "Cross-Site Request Forgery",
        "icon": "shuffle",
        "severity": "high",
        "owasp": "A01:2021 - Broken Access Control",
        "description": "Forge requests on behalf of authenticated users without their knowledge.",
        "url": "/vuln/csrf/",
    },
    {
        "id": "idor",
        "name": "Insecure Direct Object Reference",
        "icon": "key",
        "severity": "high",
        "owasp": "A01:2021 - Broken Access Control",
        "description": "Access resources belonging to other users by manipulating identifiers.",
        "url": "/vuln/idor/",
    },
    {
        "id": "cmdi",
        "name": "Command Injection",
        "icon": "terminal",
        "severity": "critical",
        "owasp": "A03:2021 - Injection",
        "description": "Execute arbitrary system commands through unsanitized user input.",
        "url": "/vuln/cmdi/",
    },
    {
        "id": "upload",
        "name": "Unrestricted File Upload",
        "icon": "upload",
        "severity": "high",
        "owasp": "A04:2021 - Insecure Design",
        "description": "Upload malicious files due to missing or weak file validation.",
        "url": "/vuln/upload/",
    },
    {
        "id": "ssrf",
        "name": "Server-Side Request Forgery",
        "icon": "globe",
        "severity": "critical",
        "owasp": "A10:2021 - SSRF",
        "description": "Make the server issue requests to unintended internal or external resources.",
        "url": "/vuln/ssrf/",
    },
]


@bp.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", labs=VULNERABILITY_LABS, user=user)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/scoreboard")
def scoreboard():
    return render_template("scoreboard.html", labs=VULNERABILITY_LABS)
