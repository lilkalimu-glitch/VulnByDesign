# VulnByDesign

> A deliberately vulnerable web application for learning web security — built for students, pentesters, and security enthusiasts.

---

**VulnByDesign** is an intentionally insecure web application designed to teach common web vulnerabilities from the [OWASP Top 10](https://owasp.org/www-project-top-ten/). Each vulnerability is implemented as an interactive lab with hints, exploit examples, and explanations.

## Disclaimer

> **This application contains real, exploitable security vulnerabilities.**
> It is designed **exclusively** for educational use in **isolated, controlled environments**.
>
> - Do **NOT** deploy on public-facing servers or production networks.
> - Do **NOT** use the techniques learned here on systems without explicit authorization.
> - The authors are not responsible for any misuse of this software.

## Vulnerability Labs

| # | Lab | OWASP Category | Severity |
|---|-----|---------------|----------|
| 1 | **SQL Injection** | A03:2021 — Injection | Critical |
| 2 | **Cross-Site Scripting (XSS)** | A03:2021 — Injection | High |
| 3 | **Cross-Site Request Forgery (CSRF)** | A01:2021 — Broken Access Control | High |
| 4 | **Insecure Direct Object Reference (IDOR)** | A01:2021 — Broken Access Control | High |
| 5 | **Command Injection** | A03:2021 — Injection | Critical |
| 6 | **Unrestricted File Upload** | A04:2021 — Insecure Design | High |
| 7 | **Server-Side Request Forgery (SSRF)** | A10:2021 — SSRF | Critical |

Each lab includes:
- A realistic vulnerable feature to exploit
- Hints to guide your testing
- The actual SQL query or command being executed (where applicable)
- Educational context on root cause and remediation

## Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/lilkalimu-glitch/VulnByDesign.git
cd VulnByDesign
docker compose up --build
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Option 2: Run Locally

```bash
git clone https://github.com/lilkalimu-glitch/VulnByDesign.git
cd VulnByDesign
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |
| `alice` | `password` | User |
| `bob` | `letmein` | User |
| `charlie` | `qwerty` | Moderator |

## Tech Stack

- **Backend:** Python 3.12 / Flask
- **Database:** SQLite
- **Frontend:** Bootstrap 5 (dark theme), Bootstrap Icons
- **Container:** Docker / Docker Compose

## Project Structure

```
VulnByDesign/
├── app/
│   ├── __init__.py          # Application factory
│   ├── database.py          # Database init & seed data
│   ├── routes/
│   │   ├── main.py          # Dashboard & navigation
│   │   ├── auth.py          # Login / Register (SQLi, weak auth)
│   │   ├── sqli.py          # SQL Injection labs
│   │   ├── xss.py           # XSS labs (reflected, stored, DOM)
│   │   ├── csrf.py          # CSRF labs
│   │   ├── idor.py          # IDOR labs
│   │   ├── cmdi.py          # Command Injection labs
│   │   ├── upload.py        # File Upload lab
│   │   └── ssrf.py          # SSRF labs
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, uploads
├── db/                      # SQLite database (auto-generated)
├── tests/                   # Test suite
├── run.py                   # Entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build
├── docker-compose.yml       # Container orchestration
└── README.md
```

## Contributing

Contributions are welcome! Ideas for new labs, bug fixes, and documentation improvements are all appreciated.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-lab`)
3. Commit your changes
4. Push to the branch and open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by projects like [DVWA](https://github.com/digininja/DVWA), [OWASP WebGoat](https://owasp.org/www-project-webgoat/), and [Juice Shop](https://owasp.org/www-project-juice-shop/).
