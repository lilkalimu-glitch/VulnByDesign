"""
Command Injection lab.

VULNERABILITIES:
  - OS command injection via subprocess with shell=True
  - Unsanitized user input passed directly to system commands
"""

import subprocess

from flask import Blueprint, render_template, request

bp = Blueprint("cmdi", __name__)


@bp.route("/")
def index():
    return render_template("labs/cmdi.html")


@bp.route("/ping", methods=["GET", "POST"])
def ping():
    """Ping a host - vulnerable to command injection."""
    output = ""
    host = request.form.get("host", "") or request.args.get("host", "")

    if host:
        # VULN: Command injection via shell=True and unsanitized input
        # An attacker can use ; | && || ` $() to chain commands
        try:
            result = subprocess.run(
                f"ping -c 3 {host}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Command timed out."
        except Exception as e:
            output = f"Error: {e}"

    return render_template("labs/cmdi_ping.html", output=output, host=host)


@bp.route("/dns", methods=["GET", "POST"])
def dns_lookup():
    """DNS lookup - vulnerable to command injection."""
    output = ""
    domain = request.form.get("domain", "") or request.args.get("domain", "")

    if domain:
        # VULN: Same pattern - unsanitized input in shell command
        try:
            result = subprocess.run(
                f"nslookup {domain}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Command timed out."
        except Exception as e:
            output = f"Error: {e}"

    return render_template("labs/cmdi_dns.html", output=output, domain=domain)
