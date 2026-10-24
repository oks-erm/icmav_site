# ─── Etapa 1: Build do Frontend (Vue 3 / Vite) ───────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ─── Etapa 2: Backend FastAPI + Produção ─────────────────────
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt uvloop httptools

# Copiar a aplicação FastAPI
COPY backend/app ./app

# Copiar os ficheiros compilados do Frontend da Etapa 1
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

# Porta padrão do Google Cloud Run (8080)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Healthcheck automático para Docker / Coolify
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -fsS http://127.0.0.1:${PORT:-8080}/api/health || exit 1

# Iniciar servidor Uvicorn com porta dinâmica do Cloud Run
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
