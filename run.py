#!/usr/bin/env python3
"""
VulnByDesign - Entry point.

WARNING: This application is intentionally vulnerable.
         Run only in isolated environments for educational purposes.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  VulnByDesign - Intentionally Vulnerable Web Application")
    print("  WARNING: Do NOT expose this to the internet!")
    print("=" * 60)
    print(f"\n  Running at: http://127.0.0.1:5000")
    print(f"  Default login: admin / admin123\n")

    app.run(host="0.0.0.0", port=5000, debug=True)
