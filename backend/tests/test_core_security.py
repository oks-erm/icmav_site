"""Security regressions using an isolated application copy and disposable database."""
import importlib
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from unittest.mock import patch

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Session


class CoreSecurityTests(unittest.TestCase):
    def test_login_limiter_bounds_clients_and_expires_old_entries(self):
        self.auth._login_attempts.clear()
        try:
            with patch.object(self.auth, 'MAX_LOGIN_CLIENTS', 2), patch.object(self.auth.time, 'monotonic', return_value=1000):
                self.auth.check_login_rate_limit('first')
                self.auth.check_login_rate_limit('second')
                with self.assertRaises(HTTPException) as caught:
                    self.auth.check_login_rate_limit('third')
                self.assertEqual(caught.exception.status_code, 429)
                self.assertEqual(len(self.auth._login_attempts), 2)
            with patch.object(self.auth.time, 'monotonic', return_value=1301):
                self.auth.check_login_rate_limit('third')
                self.assertEqual(len(self.auth._login_attempts), 1)
        finally:
            self.auth._login_attempts.clear()

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="icmav-core-security-")
        cls.root = Path(cls.tmp.name)
        cls.package = cls.root / "core_security_app"
        shutil.copytree(Path(__file__).resolve().parents[1] / "app", cls.package,
                        ignore=shutil.ignore_patterns("uploads", "__pycache__"))
        cls.dist = cls.root / "frontend_dist"
        cls.dist.mkdir()
        (cls.dist / "index.html").write_text("<html>Public SPA</html>")
        (cls.dist / "favicon.ico").write_bytes(b"public-icon")
        cls.outside = cls.root / "private-fixture.txt"
        cls.outside.write_text("private fixture must never be served")
        (cls.dist / "linked-secret.txt").symlink_to(cls.outside)
        cls.password = secrets.token_urlsafe(24)
        cls.environment = {
            "ADMIN_USERNAME": "test-admin",
            "ADMIN_PASSWORD_HASH": bcrypt.hashpw(cls.password.encode(), bcrypt.gensalt(4)).decode(),
            "JWT_SECRET": secrets.token_urlsafe(48),
            "JWT_EXPIRE_MINUTES": "120",
            "PYTHON_DOTENV_DISABLED": "1",
            "ICMAV_DATA_DIR": str(cls.root / "data"),
            "CORS_ORIGINS": "http://localhost:5173",
        }
        cls.env_patch = patch.dict(os.environ, cls.environment)
        cls.env_patch.start()
        sys.path.insert(0, str(cls.root))
        cls.metadata_patch = patch.object(SQLModel, "metadata", MetaData())
        cls.metadata_patch.start()
        cls.auth = importlib.import_module("core_security_app.auth")
        cls.main = importlib.import_module("core_security_app.main")
        @cls.main.app.get("/api/security-test-error")
        def error_fixture():
            raise RuntimeError("Test error")

        cls.main.app.router.routes.insert(0, cls.main.app.router.routes.pop())
        cls.client_context = TestClient(cls.main.app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        importlib.import_module("core_security_app.database").engine.dispose()
        sys.path.remove(str(cls.root))
        for name in list(sys.modules):
            if name == "core_security_app" or name.startswith("core_security_app."):
                sys.modules.pop(name)
        cls.metadata_patch.stop()
        cls.env_patch.stop()
        cls.tmp.cleanup()

    def test_startup_rejects_missing_or_invalid_auth_configuration(self):
        cases = [
            {"JWT_SECRET": ""}, {"JWT_SECRET": "too-short"},
            {"ADMIN_PASSWORD_HASH": ""}, {"ADMIN_PASSWORD_HASH": "not-bcrypt"},
            {"ADMIN_USERNAME": ""}, {"JWT_EXPIRE_MINUTES": "0"},
            {"JWT_EXPIRE_MINUTES": "-1"}, {"JWT_EXPIRE_MINUTES": "not-a-number"},
        ]
        for overrides in cases:
            with self.subTest(configuration=list(overrides)):
                result = subprocess.run(
                    [sys.executable, "-c", "import core_security_app.auth"],
                    cwd=self.root, env={**os.environ, **self.environment, **overrides},
                    capture_output=True, text=True, timeout=10,
                )
                self.assertNotEqual(result.returncode, 0, "Unsafe authentication config was accepted")
                self.assertNotIn(self.environment["JWT_SECRET"], result.stderr)
                self.assertNotIn(self.environment["ADMIN_PASSWORD_HASH"], result.stderr)

    def test_tokens_require_valid_expiry_and_admin_subject(self):
        cases = [
            {"sub": "test-admin"}, {"exp": time.time() + 300},
            {"sub": "test-admin", "exp": None},
            {"sub": "test-admin", "exp": "9999999999"},
            {"sub": "test-admin", "exp": float("nan")},
            {"sub": "test-admin", "exp": time.time() - 300},
            {"sub": "someone-else", "exp": time.time() + 300},
        ]
        for payload in cases:
            with self.subTest(payload=payload):
                token = jwt.encode(payload, self.environment["JWT_SECRET"], algorithm="HS256")
                with self.assertRaises(HTTPException) as raised:
                    self.auth.get_current_admin(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
                self.assertEqual(raised.exception.status_code, 401)

    def test_login_and_issued_token_preserve_contract(self):
        response = self.client.post("/api/admin/login", json={"username": "test-admin", "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")
        token = response.json()["access_token"]
        self.assertEqual(self.auth.get_current_admin(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)), "test-admin")
        self.assertEqual(response.headers.get("cache-control"), "private, no-store")

    def test_spa_rejects_parent_absolute_and_symlink_escape(self):
        for path in ["/%2e%2e/private-fixture.txt", "/%2F" + str(self.outside).lstrip("/"), "/linked-secret.txt"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                self.assertNotIn("private fixture", response.text)
        self.assertEqual(self.client.get("/favicon.ico").content, b"public-icon")
        self.assertIn("Public SPA", self.client.get("/about/church").text)

    def test_credentials_authenticated_reads_errors_and_mutations_are_not_cached(self):
        token = self.auth.create_access_token("test-admin")
        headers = {"Authorization": "Bearer " + token}
        responses = [
            self.client.get("/api/settings/ifthenpay-config", headers=headers),
            self.client.get("/api/settings/sibs-config", headers=headers),
            self.client.get("/api/settings/welcome", headers=headers),
            self.client.get("/api/settings/ifthenpay-config"),
            self.client.get("/uploads/missing.png"),
            self.client.put("/api/settings/welcome", json={"content": "change"}),
        ]
        for response in responses:
            with self.subTest(path=response.request.url.path, status=response.status_code):
                self.assertEqual(response.headers.get("cache-control"), "private, no-store")

    def test_public_content_cache_and_security_headers(self):
        response = self.client.get("/api/settings/welcome")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers.get("cache-control", "").startswith("public,"))
        for path in ["/", "/api/settings/welcome", "/uploads/missing.png"]:
            with self.subTest(path=path):
                headers = self.client.get(path).headers
                self.assertEqual(headers.get("x-content-type-options"), "nosniff")
                self.assertEqual(headers.get("referrer-policy"), "strict-origin-when-cross-origin")
                self.assertEqual(headers.get("x-frame-options"), "DENY")

    def test_unhandled_errors_and_cors_rejections_have_security_headers(self):
        with TestClient(self.main.app, raise_server_exceptions=False) as client:
            responses = [
                client.get("/api/security-test-error"),
                client.options("/api/settings/welcome", headers={
                    "Origin": "https://untrusted.invalid",
                    "Access-Control-Request-Method": "GET",
                }),
            ]
        self.assertEqual(responses[0].status_code, 500)
        self.assertEqual(responses[1].status_code, 400)
        for response in responses:
            with self.subTest(status=response.status_code):
                self.assertEqual(response.headers.get("cache-control"), "private, no-store")
                self.assertEqual(response.headers.get("x-content-type-options"), "nosniff")

    def test_payment_validation_marks_only_new_attempts_not_sent_and_preserves_error_contract(self):
        payload = {"amount": "0.00", "phone": "912345678"}
        response = self.client.post("/api/donate/mbway", json=payload, headers={
            "Idempotency-Key": str(uuid.uuid4()),
            "Origin": "http://localhost:5173",
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.headers.get("x-payment-attempt-state"), "not-sent")
        self.assertEqual(response.headers.get("cache-control"), "private, no-store")
        self.assertEqual(response.headers.get("access-control-allow-origin"), "http://localhost:5173")
        exposed = {value.strip().lower() for value in response.headers["access-control-expose-headers"].split(",")}
        self.assertTrue({"x-payment-attempt-state", "retry-after"}.issubset(exposed))
        original_error = response.json()
        self.assertEqual(set(original_error), {"detail"})
        self.assertEqual(original_error["detail"][0]["loc"], ["body", "amount"])
        self.assertEqual(original_error["detail"][0]["type"], "greater_than")

        model = importlib.import_module("core_security_app.models").PaymentAttempt
        for state in ("pending", "unknown", "ready"):
            with self.subTest(state=state):
                key = str(uuid.uuid4())
                with Session(self.main.engine) as session:
                    session.add(model(
                        key=key, fingerprint="test-input", client_fingerprint="test-client",
                        phone_fingerprint="test-phone", created_at=time.time(),
                        order_id="test-order", state=state,
                    ))
                    session.commit()
                existing = self.client.post("/api/donate/mbway", json=payload,
                                            headers={"Idempotency-Key": key})
                self.assertEqual(existing.status_code, 422)
                self.assertIsNone(existing.headers.get("x-payment-attempt-state"))
                self.assertEqual(existing.json(), original_error)


if __name__ == "__main__":
    unittest.main()
