"""
Server-Side Request Forgery (SSRF) lab.

VULNERABILITIES:
  - Unrestricted URL fetching from user input
  - No allowlist/blocklist for target hosts
  - Internal network accessible via crafted URLs
"""

import urllib.request
import urllib.error

from flask import Blueprint, render_template, request

bp = Blueprint("ssrf", __name__)


@bp.route("/")
def index():
    return render_template("labs/ssrf.html")


@bp.route("/fetch", methods=["GET", "POST"])
def fetch_url():
    """Fetch a URL provided by the user - no restrictions."""
    content = ""
    error = None
    url = request.form.get("url", "") or request.args.get("url", "")

    if url:
        # VULN: No URL validation or allowlist
        # Attacker can request internal services: http://localhost:8080/admin
        # Or cloud metadata: http://169.254.169.254/latest/meta-data/
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VulnByDesign/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode("utf-8", errors="replace")[:5000]
        except urllib.error.URLError as e:
            error = f"URL Error: {e.reason}"
        except Exception as e:
            error = f"Error: {e}"

    return render_template("labs/ssrf_fetch.html", content=content, url=url, error=error)


@bp.route("/webhook", methods=["GET", "POST"])
def webhook():
    """Configure a webhook URL - SSRF via callback."""
    status = None
    url = request.form.get("webhook_url", "") or request.args.get("webhook_url", "")

    if url:
        # VULN: Webhook URL not validated - can target internal services
        try:
            data = b'{"event": "test", "message": "ping"}'
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                status = f"Webhook delivered: HTTP {response.status}"
        except Exception as e:
            status = f"Webhook delivery failed: {e}"

    return render_template("labs/ssrf_webhook.html", status=status, url=url)
