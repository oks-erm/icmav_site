"""
main.py — Ponto de entrada da aplicação FastAPI com inicialização limpa, compressão GZip e cache control.
"""

import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from sqlmodel import Session

from .database import create_db_and_tables, engine
from .payment_attempts import attempt_was_started
from .defaults import UPLOADS_DIR
from .colormanagement import TAILWIND_ALLOWED_COLORS
from .request_limits import RequestBodyLimitMiddleware
from .auth import get_current_admin
from .routers import auth, settings, donations

logger = logging.getLogger("icmav_api")

# ─── Lifespan ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# ─── App FastAPI ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="ICMAV Website API",
    description="API para gestão de conteúdos e pagamentos do site da ICMAV",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Compressão GZip (respostas >= 1KB) ───────────────────────────────────────

app.add_middleware(GZipMiddleware, minimum_size=1000)


def authorize_upload(scope: dict) -> bool:
    """Authenticate upload headers before accepting their large request bodies."""
    headers = [value for name, value in scope.get("headers", []) if name.lower() == b"authorization"]
    if len(headers) != 1 or len(headers[0]) > 8192:
        return False
    try:
        scheme, separator, token = headers[0].decode("ascii").partition(" ")
        if scheme.lower() != "bearer" or not separator or not token or token != token.strip():
            return False
        get_current_admin(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
    except (UnicodeError, HTTPException):
        return False
    return True


app.add_middleware(RequestBodyLimitMiddleware, upload_authorizer=authorize_upload)

# ─── Configuração de CORS ────────────────────────────────────────────────────

_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Payment-Attempt-State", "Retry-After"],
)

# ─── Middleware de Cache-Control HTTP ────────────────────────────────────────

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
}

PUBLIC_SETTINGS_PATHS = {
    f"/api/settings/{section}"
    for section in (
        "welcome", "purposes", "pastoral-team", "message", "ministries-presentation",
        "services-banner", "local-gatherings", "local-gathering-options", "gallery",
        "social-media", "donations", "locations", "google-maps-config",
    )
}


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response: Response = await call_next(request)

    # Só conteúdos explicitamente públicos podem entrar em caches partilhadas.
    response.headers["Cache-Control"] = "private, no-store"
    if (
        request.method in {"GET", "HEAD"}
        and 200 <= response.status_code < 300
        and "authorization" not in request.headers
        and "cookie" not in request.headers
        and "set-cookie" not in response.headers
    ):
        path = request.url.path
        if path.startswith("/uploads/"):
            response.headers["Cache-Control"] = "public, max-age=86400"
        elif path in PUBLIC_SETTINGS_PATHS:
            response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=300"
        elif path == "/api/health":
            response.headers["Cache-Control"] = "no-cache"

    response.headers.update(SECURITY_HEADERS)
    return response

@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    # O middleware de erros do Starlette é exterior aos middlewares da aplicação.
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers={**SECURITY_HEADERS, "Cache-Control": "private, no-store"},
    )


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    response = await request_validation_exception_handler(request, exc)
    if request.method == "POST" and request.url.path == "/api/donate/mbway":
        with Session(engine) as session:
            if not attempt_was_started(session, request.headers.get("Idempotency-Key")):
                response.headers["X-Payment-Attempt-State"] = "not-sent"
    return response


# ─── Ficheiros Estáticos (Uploads) ───────────────────────────────────────────

app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# ─── Routers ─────────────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(donations.router)

# ─── Health Check ────────────────────────────────────────────────────────────

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "icmav-api"}

# ─── Servir Frontend Vue SPA (Produção / Cloud Run) ──────────────────────────

from fastapi.responses import FileResponse

frontend_dist = Path(__file__).resolve().parent.parent / "frontend_dist"
if not frontend_dist.exists():
    frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if frontend_dist.exists():
    frontend_dist = frontend_dist.resolve()
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Se for um ficheiro estático existente na raiz do dist (ex: favicon, robots.txt)
        try:
            file_path = (frontend_dist / full_path).resolve()
            file_path.relative_to(frontend_dist)
        except (ValueError, OSError, RuntimeError):
            raise HTTPException(status_code=404, detail="Not found") from None
        if full_path and file_path.is_file():
            return FileResponse(file_path)
        # Fallback para o index.html da SPA (Vue Router)
        index_path = (frontend_dist / "index.html").resolve()
        if not index_path.is_relative_to(frontend_dist) or not index_path.is_file():
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(index_path)
