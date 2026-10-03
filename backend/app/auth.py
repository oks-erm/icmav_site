"""
auth.py — Autenticação JWT, hash de passwords com bcrypt e rate limiting para login.
"""

import os
import time
import logging
import hashlib
import math
import re
from collections import OrderedDict
from threading import Lock
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# ─── Configuração ────────────────────────────────────────────────────────────

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "").strip()
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

# Fingerprints reject credentials previously distributed in the repository.
_REVOKED_JWT_SECRET_DIGESTS = frozenset({'fceddf58450eccefaac733824908a4f713f5febf5ac8ec115ffa0b652a9b0bec', 'a466b6a31c723f3e8810ff3165f5fecdd105b386e85be2df9f96120a804c5657'})
_REVOKED_PASSWORD_HASH_DIGEST = "654c57b2bfd171db1886739e550e2d77a4b69b9bae222d2ed16166d88cb9908b"


def validate_auth_configuration() -> int:
    """Fail closed before accepting requests; never include secret values in errors."""
    if (
        len(JWT_SECRET.encode("utf-8")) < 32
        or not JWT_SECRET.strip()
        or hashlib.sha256(JWT_SECRET.encode()).hexdigest() in _REVOKED_JWT_SECRET_DIGESTS
    ):
        raise RuntimeError("JWT_SECRET must be a new randomly generated secret of at least 32 bytes.")
    if not ADMIN_USERNAME:
        raise RuntimeError("ADMIN_USERNAME must be configured.")
    if (
        not re.fullmatch(r"\$2[aby]\$(0[4-9]|[12][0-9]|3[01])\$[./A-Za-z0-9]{53}", ADMIN_PASSWORD_HASH)
        or hashlib.sha256(ADMIN_PASSWORD_HASH.encode()).hexdigest() == _REVOKED_PASSWORD_HASH_DIGEST
    ):
        raise RuntimeError("ADMIN_PASSWORD_HASH must be a bcrypt hash for a new private password.")
    try:
        expiry = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))
    except ValueError:
        raise RuntimeError("JWT_EXPIRE_MINUTES must be a positive integer.") from None
    if not 1 <= expiry <= 1440:
        raise RuntimeError("JWT_EXPIRE_MINUTES must be between 1 and 1440.")
    return expiry


JWT_EXPIRE_MINUTES = validate_auth_configuration()

# ─── Esquema Bearer ───────────────────────────────────────────────────────────

bearer_scheme = HTTPBearer(auto_error=True)

# ─── Rate limiting simples (in-memory) ───────────────────────────────────────
# Máximo LOGIN_MAX_ATTEMPTS tentativas por IP em LOGIN_WINDOW_SECONDS segundos.

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutos
MAX_LOGIN_CLIENTS = 10_000

_login_attempts: dict[str, list[float]] = OrderedDict()
_login_lock = Lock()


def check_login_rate_limit(ip: str) -> None:
    now = time.monotonic()
    window_start = now - LOGIN_WINDOW_SECONDS

    with _login_lock:
        # Ordered by last accepted attempt: expire stale clients without scanning all.
        while _login_attempts and next(iter(_login_attempts.values()))[-1] <= window_start:
            _login_attempts.popitem(last=False)
        attempts = [t for t in _login_attempts.get(ip, []) if t > window_start]
        if len(attempts) >= LOGIN_MAX_ATTEMPTS or (ip not in _login_attempts and len(_login_attempts) >= MAX_LOGIN_CLIENTS):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Demasiadas tentativas de login. Tenta novamente em {LOGIN_WINDOW_SECONDS // 60} minutos.",
                headers={"Retry-After": str(LOGIN_WINDOW_SECONDS)},
            )
        attempts.append(now)
        _login_attempts[ip] = attempts
        _login_attempts.move_to_end(ip)


# ─── Funções de password (bcrypt nativo) ──────────────────────────────────────

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        logger.warning("Não foi possível verificar a password fornecida.")
        return False


def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


# ─── Funções JWT ──────────────────────────────────────────────────────────────

def create_access_token(username: str) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET não está definido nas variáveis de ambiente.")

    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    """Dependência FastAPI: valida o token JWT e devolve o username do admin."""
    token = credentials.credentials

    if not JWT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Servidor não configurado corretamente.",
        )

    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        expiry = payload["exp"]
        if isinstance(expiry, bool) or not isinstance(expiry, (int, float)) or not math.isfinite(expiry):
            raise InvalidTokenError("Invalid expiry")
        username: str | None = payload.get("sub")
    except (InvalidTokenError, TypeError, ValueError, OverflowError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not username or username != ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não autorizado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username
