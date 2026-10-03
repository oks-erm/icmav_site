# ICMAV website

## Purpose and structure
Public Portuguese-language church website, content backoffice, and IFTHENPAY MB WAY donations.
- `frontend/`: Vue 3/Vite/Tailwind, Vue Router, components, API client, and Node tests.
- `backend/app/`: FastAPI routers, validation, SQLModel persistence, authentication, gateway client, and encrypted settings.
- `backend/tests/`: unittest security/integration regressions; no real provider requests.
- `backend/scripts/init_secrets.py`: creates private local credentials without overwriting existing files.
- `Dockerfile`: builds frontend, serves it through the Python API.

## Setup and checks
Python 3.12+ and Node 20+ are required.
```
python3.12 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
backend/.venv/bin/python backend/scripts/init_secrets.py
cd frontend && npm ci && npm test && npm run build
```
From the repository root, backend tests run with:
```
PYTHONPATH=backend backend/.venv/bin/python -m unittest discover -s backend/tests -v
```
For development, run `uvicorn app.main:app --reload` from `backend/` with the virtual environment active, and `npm run dev` from `frontend/`.
Vite proxies `/api` and `/uploads` to localhost:8000; production API requests use the same origin by default.
No separate lint/typecheck commands or CI workflows are currently configured.

## Secrets and data
- Never commit, print, or include `.env`, `.local-state`, `.local-backups`, databases, uploads, credentials, or deployment scripts in Docker builds.
- `backend/.env` supplies explicit admin username, bcrypt password hash, JWT signing secret, and `SETTINGS_ENCRYPTION_KEY` (Fernet).
- Keep secret files owner-readable/writable only (0600), directories private (0700). Back up the encryption key separately from public release files. Do not rotate or discard it without a migration/recovery plan.
- `ICMAV_DATA_DIR` selects the private runtime directory containing SQLite and uploads; use an actual persistent local volume in production, outside the web root.
- Without that override, legacy local paths remain in use. Moving the directory requires copying the database and uploads first; setting a different empty path does not migrate content.
- Startup creates additive SQLModel tables and encrypts legacy merchant credential fields transactionally. Existing backups may still contain plaintext credentials and must remain private.
- Settings reads return detached decrypted objects so unrelated commits cannot persist plaintext. Write settings through `crud.upsert_setting`.
- IFTHENPAY keys are configured in the authenticated backoffice; only the canonical HTTPS provider origin is permitted. Google Maps browser keys must be restricted by domain/API at the provider.
- PaymentAttempt is an additive SQLite table with durable UUID claims, HMAC input/phone/client fingerprints, safe provider results and poll state. Never remove claims to retry a payment. Initiation reserves before transport; unknown results require treasury reconciliation. One durable SQLite database must serve all requests; do not deploy replicas with separate ephemeral databases.
- Payment POSTs require UUID v4 `Idempotency-Key`; recovery/status require the same key. Only explicit `X-Payment-Attempt-State: not-sent` permits correction/retry with that same UUID and `Retry-After`. Never infer no debit from a timeout, HTTP status alone, or ambiguous provider message. Confirmed success is terminal even with out-of-order polling.

## Safety and deployment
- Keep user-facing Portuguese copy in Portuguese.
- Never test real payments or send notifications as part of validation. Mock only the external transport.
- Maintain HTML sanitization, file containment checks, private/no-store headers, explicit authentication, and response validation.
- Preserve all existing uncommitted work. Never force-push or delete user files without explicit approval.
- Production deployment and changes to hosting require user authorization and a verified backup.
- The local FTP script is outside this checkout and must remain uncommitted. FTP uploads alone cannot install/start FastAPI.
- Verified WebHS HS S account features currently disable Python apps, Passenger and SSH. Full backend deployment needs provider enablement or a separate suitable host. Never claim a static upload deployed the backend.
- Containers need durable database/upload storage; an ordinary Cloud Run writable filesystem is not durable.

## Known limitations and validation checklist
Help/group forms remain frontend placeholders with no submission backend. Do not claim delivery is implemented.
The fiscal receipt workflow is not implemented; do not promise automatic issuance.
The npm audit still reports the unpatched Quill 2.0.3 HTML-export advisory. Video/formula formats are disabled, HTML is sanitized on input/render/output, and regression tests enforce this. Do not downgrade to hide the advisory; revisit when an upstream fix exists.
Login throttling is per process; use a trusted reverse proxy and edge rate limiting in production, and do not trust arbitrary forwarded client IP headers. Payment initiation has durable phone/IP/global throttling; status polling is also bounded.
Before release: run frontend tests/build, full backend tests, inspect the diff for secrets, check deployment compatibility, validate backup/recovery, verify HTTPS/API/static files and logs after deployment. Keep the PR unmerged if release blockers remain.
