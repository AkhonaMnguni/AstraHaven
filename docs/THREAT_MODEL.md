# Threat Model

## Assets

Credentials, transaction amounts, supplier relationships, alert records, and audit events.

## Threats

- Credential guessing and session theft.
- Unauthorized role escalation.
- Tampering with transaction or alert state.
- Sensitive data exposure through logs or error pages.

## Controls

Passwords are stored with Werkzeug password hashing. Access is protected by Flask-Login and explicit role checks. Production deployments must use a strong secret key, HTTPS, secure cookies, rate limiting, and centralized audit storage.
