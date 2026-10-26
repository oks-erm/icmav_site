"""
main.py — Ponto de entrada da aplicação FastAPI com inicialização limpa, compressão GZip e cache control.
"""

import gzip
import json
import mimetypes
import os
import re
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from starlette.datastructures import Headers, MutableHeaders
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
    _preload_frontend_dist()
    yield

# ─── App FastAPI ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="ICMAV Website API",
    description="API para gestão de conteúdos e pagamentos do site da ICMAV",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Compressão GZip seletiva (respostas textuais >= 1KB, nível 5) ───────────

GZIP_SKIP_PREFIXES = ("/videos/", "/photos/", "/fallbacks/", "/uploads/")
GZIP_SKIP_SUFFIXES = (
    ".mp4", ".webm", ".webp", ".png", ".jpg", ".jpeg", ".gif", ".woff2", ".woff", ".ico",
)


class SelectiveGZipMiddleware:
    """Aplica GZip rápido apenas a respostas textuais/API sem cabeçalho Range."""

    def __init__(self, app, minimum_size: int = 1000, compresslevel: int = 5):
        self.app = app
        self.gzip_app = GZipMiddleware(app, minimum_size=minimum_size, compresslevel=compresslevel)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = (scope.get("path") or "").lower()
        has_range = any(name.lower() == b"range" for name, _ in scope.get("headers", []))
        if has_range or path.startswith(GZIP_SKIP_PREFIXES) or path.endswith(GZIP_SKIP_SUFFIXES):
            await self.app(scope, receive, send)
            return
        await self.gzip_app(scope, receive, send)


app.add_middleware(SelectiveGZipMiddleware, minimum_size=1000, compresslevel=5)


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
        "public-bootstrap",
        "welcome", "purposes", "pastoral-team", "message", "ministries-presentation",
        "services-banner", "local-gatherings", "local-gathering-options", "gallery",
        "social-media", "donations", "locations", "google-maps-config",
    )
}

PUBLIC_STATIC_PREFIXES = ("/photos/", "/fallbacks/", "/videos/")
PUBLIC_STATIC_FILES = {"/favicon.ico", "/logo_provisory_white.png", "/logo_provisory_black.png"}


class CacheAndSecurityHeadersMiddleware:
    """Middleware ASGI puro para cabeçalhos de segurança e Cache-Control."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        req_headers = Headers(scope=scope)
        method = scope.get("method", "GET")
        path = scope.get("path", "")
        is_unauthenticated_read = (
            method in {"GET", "HEAD"}
            and "authorization" not in req_headers
            and "cookie" not in req_headers
        )

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                status_code = message.get("status", 200)
                res_headers = MutableHeaders(raw=message["headers"])
                res_headers["Cache-Control"] = "private, no-store"
                if (
                    is_unauthenticated_read
                    and 200 <= status_code < 300
                    and "set-cookie" not in res_headers
                ):
                    if path.startswith("/uploads/"):
                        res_headers["Cache-Control"] = "public, max-age=86400"
                    elif path.startswith("/assets/"):
                        res_headers["Cache-Control"] = "public, max-age=31536000, immutable"
                    elif (
                        (path.startswith(PUBLIC_STATIC_PREFIXES) or path in PUBLIC_STATIC_FILES)
                        and not res_headers.get("content-type", "").startswith("text/html")
                    ):
                        res_headers["Cache-Control"] = "public, max-age=86400, stale-while-revalidate=604800"
                    elif path in PUBLIC_SETTINGS_PATHS:
                        res_headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=300"
                    elif path == "/api/health":
                        res_headers["Cache-Control"] = "no-cache"

                for header_name, header_value in SECURITY_HEADERS.items():
                    res_headers[header_name] = header_value

            await send(message)

        await self.app(scope, receive, send_with_headers)


app.add_middleware(CacheAndSecurityHeadersMiddleware)

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

_spa_index_cache: tuple[str, int, str, str, bytes] | None = None
_static_ram_cache: dict[str, tuple[int, str, bytes, bytes | None]] = {}
_CSS_LINK_RE = re.compile(r'<link\s+rel="stylesheet"\s+crossorigin\s+href="(/assets/[^"]+\.css)"\s*/?>')
_COMPRESSIBLE_EXTS = {".js", ".css", ".svg", ".html", ".json", ".txt", ".xml"}
_MAX_RAM_CACHE_FILE_BYTES = 2 * 1024 * 1024


def _get_initial_donations_script() -> str:
    try:
        from .crud import _public_cache, get_setting
        from .defaults import DEFAULT_DONATIONS_CONTENT
        cached = _public_cache.get((id(engine), "donations_content"))
        if cached is not None:
            raw_val = cached[1]
        else:
            with Session(engine) as session:
                setting = get_setting(session, "donations_content")
                raw_val = setting.value if setting else json.dumps(DEFAULT_DONATIONS_CONTENT, ensure_ascii=False)
        parsed = json.loads(raw_val)
    except Exception:
        from .defaults import DEFAULT_DONATIONS_CONTENT
        parsed = DEFAULT_DONATIONS_CONTENT
    payload = json.dumps({"key": "donations_content", "value": parsed}, ensure_ascii=False)
    safe_payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return f"<script>window.__INITIAL_DONATIONS__={safe_payload};</script>"


def _read_cached_index_html(index_path: Path) -> tuple[str, bytes]:
    global _spa_index_cache
    stat_mtime = index_path.stat().st_mtime_ns
    path_key = str(index_path)
    donations_script = _get_initial_donations_script()
    if (
        _spa_index_cache is not None
        and _spa_index_cache[0] == path_key
        and _spa_index_cache[1] == stat_mtime
        and _spa_index_cache[2] == donations_script
    ):
        return _spa_index_cache[3], _spa_index_cache[4]
    content = index_path.read_text(encoding="utf-8")
    dist_root = index_path.parent.resolve()

    def _inline_css(match: re.Match) -> str:
        rel_href = match.group(1).lstrip("/")
        try:
            css_file = (dist_root / rel_href).resolve()
            css_file.relative_to(dist_root)
            if css_file.is_file():
                css_text = css_file.read_text(encoding="utf-8")
                return f"<style>{css_text}</style>"
        except (ValueError, OSError, RuntimeError):
            pass
        return match.group(0)

    content = _CSS_LINK_RE.sub(_inline_css, content)
    if "</head>" in content:
        content = content.replace("</head>", f"{donations_script}</head>", 1)
    raw_bytes = content.encode("utf-8")
    gz_bytes = gzip.compress(raw_bytes, compresslevel=9) if len(raw_bytes) >= 1000 else raw_bytes
    _spa_index_cache = (path_key, stat_mtime, donations_script, content, gz_bytes)
    return content, gz_bytes


def _serve_ram_or_file(file_path: Path, request: Request | None) -> Response:
    stat = file_path.stat()
    if stat.st_size > _MAX_RAM_CACHE_FILE_BYTES:
        return FileResponse(file_path, stat_result=stat)
    key = str(file_path)
    cached = _static_ram_cache.get(key)
    if cached is None or cached[0] != stat.st_mtime_ns:
        raw_bytes = file_path.read_bytes()
        media_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        ext = file_path.suffix.lower()
        gz_bytes = (
            gzip.compress(raw_bytes, compresslevel=9)
            if ext in _COMPRESSIBLE_EXTS and len(raw_bytes) >= 1000
            else None
        )
        if gz_bytes is not None and len(gz_bytes) >= len(raw_bytes):
            gz_bytes = None
        cached = (stat.st_mtime_ns, media_type, raw_bytes, gz_bytes)
        _static_ram_cache[key] = cached

    _, media_type, raw_bytes, gz_bytes = cached
    accept_encoding = request.headers.get("accept-encoding", "") if request is not None else ""
    if gz_bytes is not None and "gzip" in accept_encoding:
        return Response(
            content=gz_bytes,
            media_type=media_type,
            headers={"Content-Encoding": "gzip", "Vary": "Accept-Encoding"},
        )
    return Response(content=raw_bytes, media_type=media_type)


frontend_dist = Path(__file__).resolve().parent.parent / "frontend_dist"
if not frontend_dist.exists():
    frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

def _preload_frontend_dist() -> None:
    if not frontend_dist.exists():
        return
    idx = (frontend_dist / "index.html").resolve()
    if idx.is_relative_to(frontend_dist) and idx.is_file():
        _read_cached_index_html(idx)
    assets_root = (frontend_dist / "assets").resolve()
    if assets_root.is_dir():
        for p in assets_root.iterdir():
            if p.is_file():
                _serve_ram_or_file(p.resolve(), None)


if frontend_dist.exists():
    frontend_dist = frontend_dist.resolve()
    assets_dir = (frontend_dist / "assets").resolve()

    @app.api_route("/assets/{asset_path:path}", methods=["GET", "HEAD"])
    async def serve_asset(asset_path: str, request: Request = None):
        try:
            file_path = (assets_dir / asset_path).resolve()
            file_path.relative_to(assets_dir)
        except (ValueError, OSError, RuntimeError):
            raise HTTPException(status_code=404, detail="Not found") from None
        if not asset_path or not file_path.is_file():
            raise HTTPException(status_code=404, detail="Not found")
        return _serve_ram_or_file(file_path, request)

    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
    async def serve_spa(full_path: str, request: Request = None):
        # Se for um ficheiro estático existente na raiz do dist (ex: favicon, robots.txt)
        try:
            file_path = (frontend_dist / full_path).resolve()
            file_path.relative_to(frontend_dist)
        except (ValueError, OSError, RuntimeError):
            raise HTTPException(status_code=404, detail="Not found") from None
        if full_path and file_path.is_file():
            return _serve_ram_or_file(file_path, request)
        # Fallback para o index.html da SPA (Vue Router) servido a partir de memória com CSS crítico inlined
        index_path = (frontend_dist / "index.html").resolve()
        if not index_path.is_relative_to(frontend_dist) or not index_path.is_file():
            raise HTTPException(status_code=404, detail="Not found")
        html_str, gz_bytes = _read_cached_index_html(index_path)
        accept_encoding = request.headers.get("accept-encoding", "") if request is not None else ""
        if "gzip" in accept_encoding and len(gz_bytes) < len(html_str):
            return Response(
                content=gz_bytes,
                media_type="text/html; charset=utf-8",
                headers={"Content-Encoding": "gzip", "Vary": "Accept-Encoding"},
            )
        return HTMLResponse(html_str)
