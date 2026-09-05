"""
main.py — Ponto de entrada da aplicação FastAPI com inicialização limpa, compressão GZip e cache control.
"""

import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .database import create_db_and_tables
from .defaults import UPLOADS_DIR
from .colormanagement import TAILWIND_ALLOWED_COLORS
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

# ─── Middleware de Cache-Control HTTP ────────────────────────────────────────

@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response: Response = await call_next(request)

    # Apenas para pedidos GET públicos
    if request.method == "GET":
        path = request.url.path
        if path.startswith("/uploads/"):
            # Ficheiros estáticos com cache de longa duração (1 dia)
            response.headers["Cache-Control"] = "public, max-age=86400, immutable"
        elif path.startswith("/api/settings/"):
            # Conteúdos de leitura: cache curta (60s) com revalidação em background
            response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=300"
        elif path.startswith("/api/health"):
            response.headers["Cache-Control"] = "no-cache"

    return response

# ─── Ficheiros Estáticos (Uploads) ───────────────────────────────────────────

app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# ─── Configuração de CORS ────────────────────────────────────────────────────

_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Se for um ficheiro estático existente na raiz do dist (ex: favicon, robots.txt)
        file_path = frontend_dist / full_path
        if full_path and file_path.is_file():
            return FileResponse(file_path)
        # Fallback para o index.html da SPA (Vue Router)
        return FileResponse(frontend_dist / "index.html")