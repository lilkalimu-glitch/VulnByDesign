"""
Database initialization and helpers for VulnByDesign.

Uses SQLite for simplicity. The database is intentionally initialized
with weak password storage and sample data for vulnerability demonstrations.
"""

import os
import sqlite3

from flask import g


def get_db(app=None):
    """Get the database connection for the current request."""
    if "db" not in g:
        db_path = g.get("db_path", "db/vulnbydesign.db")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize the database with schema and seed data."""
    db_path = app.config.get("DATABASE", "db/vulnbydesign.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    @app.before_request
    def before_request():
        g.db_path = db_path

    app.teardown_appcontext(close_db)

    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # --- Schema ---
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,  -- VULN: plaintext passwords
                email TEXT,
                role TEXT DEFAULT 'user',
                profile_pic TEXT DEFAULT 'default.png'
            );

            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                subject TEXT,
                body TEXT,
                read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                stock INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                total REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        """)

        # --- Seed Data ---
        # VULN: Passwords stored in plaintext
        cursor.executemany(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            [
                ("admin", "admin123", "admin@vulnbydesign.local", "admin"),
                ("alice", "password", "alice@vulnbydesign.local", "user"),
                ("bob", "letmein", "bob@vulnbydesign.local", "user"),
                ("charlie", "qwerty", "charlie@vulnbydesign.local", "moderator"),
            ],
        )

        cursor.executemany(
            "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
            [
                ("Laptop", "High-performance laptop for developers", 999.99, 50),
                ("Keyboard", "Mechanical keyboard with RGB", 149.99, 200),
                ("Mouse", "Ergonomic wireless mouse", 49.99, 300),
                ("Monitor", "27-inch 4K display", 449.99, 75),
                ("Headset", "Noise-cancelling headset", 199.99, 150),
            ],
        )

        cursor.executemany(
            "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)",
            [
                (1, "Welcome to VulnByDesign", "This is a deliberately vulnerable app for learning."),
                (2, "My first post", "Hello everyone! Excited to be here."),
                (3, "Security tips", "Always use parameterized queries... or not."),
            ],
        )

        conn.commit()
        conn.close()
