# Security Policy

## This Application is Intentionally Vulnerable

**VulnByDesign** is a deliberately insecure web application created for educational purposes. All vulnerabilities are **by design** and are not bugs.

## Do NOT Report Intentional Vulnerabilities

The following are **expected** and should **not** be reported as security issues:

- SQL Injection in search and login forms
- Cross-Site Scripting (reflected, stored, DOM-based)
- Cross-Site Request Forgery on state-changing endpoints
- Insecure Direct Object References
- OS Command Injection
- Unrestricted file uploads
- Server-Side Request Forgery
- Plaintext password storage
- Missing rate limiting
- Verbose error messages
- Session fixation

## Reporting Actual Security Issues

If you find a security issue in the **infrastructure** of this project (e.g., a vulnerability in the build pipeline, a compromised dependency, or an issue that could affect users' development machines), please open a GitHub issue.

## Responsible Use

- Only run this application in isolated, controlled environments
- Never deploy on production or public-facing infrastructure
- Do not use techniques learned here against systems without explicit authorization
