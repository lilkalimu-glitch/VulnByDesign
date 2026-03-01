"""Basic tests for VulnByDesign application."""

import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_index_loads(client):
    """Home page should return 200."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"VulnByDesign" in rv.data


def test_login_page_loads(client):
    """Login page should return 200."""
    rv = client.get("/auth/login")
    assert rv.status_code == 200
    assert b"Login" in rv.data


def test_register_page_loads(client):
    """Register page should return 200."""
    rv = client.get("/auth/register")
    assert rv.status_code == 200


def test_sqli_lab_loads(client):
    """SQL Injection lab should return 200."""
    rv = client.get("/vuln/sqli/")
    assert rv.status_code == 200


def test_xss_lab_loads(client):
    """XSS lab should return 200."""
    rv = client.get("/vuln/xss/")
    assert rv.status_code == 200


def test_csrf_lab_loads(client):
    """CSRF lab should return 200."""
    rv = client.get("/vuln/csrf/")
    assert rv.status_code == 200


def test_idor_lab_loads(client):
    """IDOR lab should return 200."""
    rv = client.get("/vuln/idor/")
    assert rv.status_code == 200


def test_cmdi_lab_loads(client):
    """Command Injection lab should return 200."""
    rv = client.get("/vuln/cmdi/")
    assert rv.status_code == 200


def test_upload_lab_loads(client):
    """File Upload lab should return 200."""
    rv = client.get("/vuln/upload/")
    assert rv.status_code == 200


def test_ssrf_lab_loads(client):
    """SSRF lab should return 200."""
    rv = client.get("/vuln/ssrf/")
    assert rv.status_code == 200


def test_sqli_search(client):
    """SQL Injection search should work with normal input."""
    rv = client.get("/vuln/sqli/search?q=Laptop")
    assert rv.status_code == 200
    assert b"Laptop" in rv.data


def test_login_with_valid_credentials(client):
    """Login should work with seeded credentials."""
    rv = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    assert rv.status_code == 200
    assert b"Welcome back" in rv.data
