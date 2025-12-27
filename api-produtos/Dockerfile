# =============================================================================
# Dockerfile para FastAPI Search Products API
# Deploy na Fly.io
# =============================================================================

# Imagem base Python
FROM python:3.11-slim-bookworm

# Variáveis de ambiente para otimizar Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (necessário para psycopg2-binary e outras libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação com uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

