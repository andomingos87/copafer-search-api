# 📚 Documentação - Search Products API

## Visão Geral

Este projeto é uma **API de busca de produtos** construída com FastAPI. Ela permite realizar buscas inteligentes em um catálogo de produtos usando múltiplas estratégias (vetorial, full-text, trigram e keyword), além de oferecer funcionalidades de integração com VTEX e cálculo de tinta.

### Principais Funcionalidades

- 🔍 **Busca Híbrida de Produtos**: Combina busca vetorial (embeddings OpenAI), full-text, trigram e keyword
- 🎨 **Estimador de Tinta**: Calcula quantidade de latas necessárias para pintura
- 🚚 **Integração VTEX**: Simulação de frete e consulta de SKUs
- 📥 **Ingestão de Dados**: Importação via CSV ou API externa (Cubo)

---

## Índice de Arquivos

### 🚀 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| [api.py](./api.md) | Servidor FastAPI com todos os endpoints da aplicação |
| [search_products.py](./search_products.md) | Lógica de busca híbrida de produtos |
| [ingest_csv.py](./ingest_csv.md) | Pipeline de ingestão de produtos via CSV |
| [ingest_api.py](./ingest_api.md) | Pipeline de ingestão via API do Cubo |

### 🛠️ Módulos de Negócio

| Arquivo | Descrição |
|---------|-----------|
| [paint_estimator.py](./paint_estimator.md) | Cálculo de quantidade de tinta e latas |
| [vtex_shipping.py](./vtex_shipping.md) | Integração com VTEX para frete |
| [vtex_client.py](./vtex_client.md) | Cliente simples para consulta VTEX |
| [image_checker.py](./image_checker.md) | Verificação de imagem adequada com IA e cache Redis |

### 📊 Utilitários de Dados

| Arquivo | Descrição |
|---------|-----------|
| [fetch_cubo_produtos.py](./fetch_cubo_produtos.md) | Consulta totais na API do Cubo |
| [head_csv.py](./head_csv.md) | Extrai primeiras N linhas de um CSV |
| [count_csv_rows.py](./count_csv_rows.md) | Conta registros de um CSV |

### 🔧 Scripts de Debug

| Arquivo | Descrição |
|---------|-----------|
| [analyze_missing_skus.py](./analyze_missing_skus.md) | Analisa SKUs perdidos na ingestão |
| [debug_pagination.py](./debug_pagination.md) | Debug de paginação da API |
| [debug_response_structure.py](./debug_response_structure.md) | Analisa estrutura de resposta da API |
| [peek_cubo_page.py](./peek_cubo_page.md) | Visualiza estrutura de uma página do Cubo |
| [test_pagination_bug.py](./test_pagination_bug.md) | Testa limites de paginação |

### 📦 Configuração

| Arquivo | Descrição |
|---------|-----------|
| [requirements.txt](./requirements.md) | Dependências Python do projeto |

---

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI (api.py)                     │
├─────────────────────────────────────────────────────────────┤
│  POST /search          │ Busca híbrida de produtos          │
│  POST /paint/estimate  │ Cálculo de tinta                   │
│  GET  /vtex/sku/{sku}  │ Consulta SKU na VTEX               │
│  POST /shipping/*      │ Simulação de frete                 │
│  POST /is-image-exists │ Verifica imagem adequada do produto│
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
    ┌────────▼────────┐          ┌─────────▼─────────┐
    │search_products.py│          │ paint_estimator.py│
    │                 │          │                   │
    │ - Busca vetorial │          │ - Cálculo área    │
    │ - Full-text     │          │ - Composição latas│
    │ - Trigram       │          └───────────────────┘
    │ - Keyword       │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │    PostgreSQL   │
    │  (pgvector/rag) │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Ingestão CSV   │ ◄── ingest_csv.py
    │  Ingestão API   │ ◄── ingest_api.py
    └─────────────────┘
```

---

## Variáveis de Ambiente

O projeto utiliza um arquivo `.env` com as seguintes variáveis:

### Banco de Dados
- `DB_HOST` - Host do PostgreSQL
- `DB_PORT` - Porta (padrão: 5432)
- `DB_USER` - Usuário
- `DB_PASSWORD` - Senha
- `DB_NAME` - Nome do banco

### OpenAI
- `OPENAI_API_KEY` - Chave de API
- `EMB_MODEL` - Modelo de embedding (padrão: text-embedding-3-small)
- `EMB_DIM` - Dimensão do embedding (padrão: 1536)

### VTEX
- `VTEX_APP_KEY` - Chave da aplicação VTEX
- `VTEX_APP_TOKEN` - Token da aplicação VTEX
- `VTEX_ACCOUNT_HOST` - Host da conta (padrão: copafer.myvtex.com)

### API Cubo
- `X_COPAFER_KEY` - Chave de acesso à API do Cubo

### Redis (Cache de Imagens)
- `REDIS_HOST` - Host do Redis (padrão: localhost)
- `REDIS_PORT` - Porta (padrão: 6379)
- `REDIS_PASSWORD` - Senha (opcional)
- `REDIS_DB` - Número do banco (padrão: 0)

### OpenRouter (IA para Seleção de Imagem)
- `OPENROUTER_API_KEY` - Bearer token para OpenRouter
- `OPENROUTER_MODEL` - Modelo a usar (padrão: openai/gpt-5-chat)

### API Copafer (Busca de Imagens)
- `COPAFER_API_BASE_URL` - URL base da API
- `COPAFER_AUTH_TOKEN` - Token de autenticação

---

## Como Iniciar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar .env
cp .env.example .env
# Editar com suas credenciais

# 3. Iniciar a API
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## Fluxo de Dados

1. **Ingestão**: Produtos são importados via CSV (`ingest_csv.py`) ou API (`ingest_api.py`)
2. **Processamento**: Texto é normalizado, dividido em chunks e convertido em embeddings
3. **Armazenamento**: Dados salvos no PostgreSQL com schema `rag`
4. **Busca**: `search_products.py` combina múltiplas estratégias para encontrar produtos
5. **API**: `api.py` expõe endpoints para busca e funcionalidades auxiliares

