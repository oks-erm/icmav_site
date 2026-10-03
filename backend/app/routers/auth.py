"""
routers/auth.py — Endpoints de autenticação administrativa.
"""

from fastapi import APIRouter, HTTPException, Request
from ..schemas import LoginRequest, TokenResponse
from ..auth import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD_HASH,
    check_login_rate_limit,
    create_access_token,
    verify_password,
)

router = APIRouter(prefix="/api/admin", tags=["Admin Auth"])


@router.post("/login", response_model=TokenResponse)
def admin_login(payload: LoginRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    check_login_rate_limit(client_ip)

    if (
        payload.username != ADMIN_USERNAME
        or not ADMIN_PASSWORD_HASH
        or not verify_password(payload.password, ADMIN_PASSWORD_HASH)
    ):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(payload.username)
    return TokenResponse(access_token=token)
