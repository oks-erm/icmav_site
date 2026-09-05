"""
auth.py — Autenticação JWT, hash de passwords com bcrypt e rate limiting para login.
"""

import os
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# ─── Configuração ────────────────────────────────────────────────────────────

DEFAULT_ADMIN_PASSWORD_HASH = "$2b$12$mx3dTPKyKmi4jh5HmZnis.wh3ogVS67AVeIjusNT.gWQXFiG/dvoO"  # hash de '1234'
JWT_SECRET = os.getenv("JWT_SECRET") or "icmav_jwt_secret_key_default_production_fallback_2025"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "SA")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH") or DEFAULT_ADMIN_PASSWORD_HASH

# ─── Esquema Bearer ───────────────────────────────────────────────────────────

bearer_scheme = HTTPBearer(auto_error=True)

# ─── Rate limiting simples (in-memory) ───────────────────────────────────────
# Máximo LOGIN_MAX_ATTEMPTS tentativas por IP em LOGIN_WINDOW_SECONDS segundos.

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutos

_login_attempts: dict[str, list[float]] = defaultdict(list)


def check_login_rate_limit(ip: str) -> None:
    now = time.monotonic()
    window_start = now - LOGIN_WINDOW_SECONDS

    # Remover tentativas fora da janela
    _login_attempts[ip] = [t for t in _login_attempts[ip] if t > window_start]

    if len(_login_attempts[ip]) >= LOGIN_MAX_ATTEMPTS:
        logger.warning("Rate limit atingido para IP: %s", ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Demasiadas tentativas de login. "
                f"Tenta novamente em {LOGIN_WINDOW_SECONDS // 60} minutos."
            ),
        )

    _login_attempts[ip].append(now)


# ─── Funções de password (bcrypt nativo) ──────────────────────────────────────

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception as exc:
        logger.error("Erro ao verificar hash de password: %s", exc)
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
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str | None = payload.get("sub")
    except InvalidTokenError:
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
