"""
VulnByDesign - A deliberately vulnerable web application for security education.

WARNING: This application contains intentional security vulnerabilities.
         DO NOT deploy this application in a production environment.
         Use only in isolated, controlled lab environments.
"""

from flask import Flask
from app.database import init_db


def create_app(config=None):
    """Application factory for VulnByDesign."""
    app = Flask(__name__)

    app.config.setdefault("SECRET_KEY", "super-secret-key-do-not-use-in-prod")
    app.config.setdefault("DATABASE", "db/vulnbydesign.db")
    app.config.setdefault("DEBUG", True)

    if config:
        app.config.update(config)

    init_db(app)

    from app.routes import auth, sqli, xss, csrf, idor, cmdi, upload, ssrf, main
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(sqli.bp, url_prefix="/vuln/sqli")
    app.register_blueprint(xss.bp, url_prefix="/vuln/xss")
    app.register_blueprint(csrf.bp, url_prefix="/vuln/csrf")
    app.register_blueprint(idor.bp, url_prefix="/vuln/idor")
    app.register_blueprint(cmdi.bp, url_prefix="/vuln/cmdi")
    app.register_blueprint(upload.bp, url_prefix="/vuln/upload")
    app.register_blueprint(ssrf.bp, url_prefix="/vuln/ssrf")

    return app
