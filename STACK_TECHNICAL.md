# Stack Técnica Recomendada - Agente Bertão (Copafer)

## 📋 Visão Geral

Este documento apresenta a stack técnica recomendada para o desenvolvimento do **Bertão**, um agente de vendas conversacional via WhatsApp, baseada em boas práticas modernas de desenvolvimento de agentes de IA (2025).

**Status Atual**: O projeto já possui uma API de produtos funcional em `api-produtos/search_products_api/` que será integrada ao agente.

---

## ✅ Componentes Já Implementados

### API de Produtos (`api-produtos/search_products_api/`)
- ✅ **FastAPI** com endpoints funcionais
- ✅ **Busca híbrida de produtos** (vetorial + full-text + trigram + keyword matching)
- ✅ **PostgreSQL + pgvector** para busca semântica
- ✅ **OpenAI Embeddings** (text-embedding-3-small)
- ✅ **Integração VTEX** para frete e produtos
- ✅ **Cálculo de tinta** (paint estimator)
- ✅ **Docker** e deploy no **Fly.io**
- ✅ **Python 3.11**

**Endpoints Disponíveis**:
- `POST /search` - Busca de produtos
- `POST /paint/estimate` - Cálculo de tinta
- `GET /vtex/sku/{sku}/productId` - Conversão SKU → ProductId
- `POST /shipping/simulate` - Simulação de frete VTEX
- `POST /shipping/simulate/slas` - SLAs de frete simplificados

**Arquitetura de Busca**:
- Busca determinística por SKU/EAN
- Busca vetorial (pgvector) com embeddings OpenAI
- Full-text search (PostgreSQL)
- Trigram matching (pg_trgm)
- Keyword matching (ILIKE/unaccent)

---

## 🎯 Requisitos Técnicos Identificados

Com base no PRD, o sistema precisa suportar:
- ✅ Integração com WhatsApp Business API
- ✅ Processamento de Linguagem Natural (NLP) avançado
- ✅ Busca semântica de produtos
- ✅ Processamento multimodal (texto, imagem, áudio, PDF)
- ✅ Gerenciamento de estado conversacional
- ✅ Integração com APIs externas (frete, pagamento, estoque)
- ✅ Persistência de dados (histórico, carrinho, clientes)
- ✅ Escalonamento inteligente para humanos
- ✅ Análise de sentimento em tempo real
- ✅ Sistema de recomendações personalizadas
- ✅ Rastreamento de métricas e analytics

---

## 🏗️ Arquitetura Recomendada

### Padrão Arquitetural: **Agentic Framework com RAG (Retrieval-Augmented Generation)**

```
┌─────────────────────────────────────────────────────────────┐
│                    WhatsApp Business API                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              API Gateway / Webhook Handler                   │
│              (FastAPI / Express.js)                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              Agent Orchestration Layer                       │
│              (LangGraph / AutoGen / CrewAI)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│   LLM Core   │ │   RAG       │ │  Tools     │
│   (Claude/   │ │   Engine    │ │  (APIs)    │
│   GPT-4)     │ │             │ │            │
└──────────────┘ └──────────────┘ └────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Data Layer                                │
│  (PostgreSQL + Vector DB + Redis + Object Storage)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Técnica Detalhada

### 1. **Linguagem de Programação**

#### **Python 3.11+** (Recomendado)
- ✅ Ecossistema maduro para IA/ML
- ✅ Bibliotecas especializadas (LangChain, LangGraph, etc.)
- ✅ Suporte nativo a processamento assíncrono
- ✅ Facilidade de integração com APIs

**Alternativa**: Node.js/TypeScript (se a equipe tiver mais expertise)

---

### 2. **Framework de Agentes de IA**

#### **LangGraph** (Recomendado - 2025)
- ✅ Framework moderno para agentes stateful
- ✅ Gerenciamento de estado conversacional nativo
- ✅ Suporte a loops e condicionais complexos
- ✅ Integração com múltiplos LLMs
- ✅ Visualização de fluxos

**Alternativas**:
- **CrewAI**: Para agentes multi-agente colaborativos
- **AutoGen**: Para conversas multi-agente
- **LangChain**: Framework mais maduro, porém menos especializado em agentes

**Exemplo de uso para Bertão**:
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    cart: dict
    customer_data: dict
    current_intent: str
    escalation_needed: bool
```

---

### 3. **Modelos de Linguagem (LLMs)**

#### **Anthropic Claude 3.5 Sonnet** (Recomendado)
- ✅ Melhor custo-benefício
- ✅ Excelente em português brasileiro
- ✅ Suporte nativo a multimodal (imagens, PDFs)
- ✅ Context window grande (200k tokens)
- ✅ Rápido e eficiente

**Alternativas**:
- **OpenAI GPT-4 Turbo**: Excelente qualidade, mais caro
- **Google Gemini Pro**: Boa alternativa, suporte multimodal
- **Open Source**: Llama 3.1, Mistral (para casos específicos)

**Estratégia Híbrida Recomendada**:
- **Claude 3.5 Sonnet**: Para conversas principais e raciocínio complexo
- **GPT-4o Mini**: Para tarefas simples e baratas (validações, formatação)
- **Embeddings**: OpenAI text-embedding-3-large ou Cohere

---

### 4. **RAG (Retrieval-Augmented Generation)**

#### **✅ PostgreSQL + pgvector** (JÁ IMPLEMENTADO)
- ✅ Já em uso no projeto
- ✅ Busca híbrida funcional (vetorial + full-text + trigram + keyword)
- ✅ Integração nativa com PostgreSQL
- ✅ Performance adequada para o volume atual
- ✅ Schema `rag` com funções otimizadas (`rag.search_vec`, `rag.search_ft`, `rag.find_by_code`)

**Alternativas para expansão futura**:
- **Qdrant**: Se precisar de escalabilidade horizontal
- **Pinecone**: Managed service, fácil de usar
- **Weaviate**: Open source, bom para produção

#### **Embeddings** (JÁ IMPLEMENTADO):
- ✅ **OpenAI text-embedding-3-small**: Em uso (configurável via `EMB_MODEL`)
- **OpenAI text-embedding-3-large**: Upgrade recomendado para melhor qualidade
- **Cohere embed-multilingual-v3**: Alternativa para português
- **BGE-M3**: Open source, multilingue

**Uso no Bertão**:
- ✅ Busca semântica de produtos (já funcional)
- 🔄 Busca de perguntas frequentes (a implementar)
- 🔄 Recomendações baseadas em histórico (a implementar)

---

### 5. **API Framework**

#### **✅ FastAPI** (JÁ IMPLEMENTADO)
- ✅ Alta performance (async nativo)
- ✅ Documentação automática (OpenAPI/Swagger)
- ✅ Validação de dados com Pydantic
- ✅ Type hints nativos
- ✅ WebSockets para real-time (suporte disponível)

**Status**: API de produtos já funcional em `api-produtos/search_products_api/api.py`

**Estrutura atual**:
```
api-produtos/search_products_api/
  api.py                    # FastAPI app principal
  search_products.py        # Busca híbrida de produtos
  vtex_client.py           # Cliente VTEX
  vtex_shipping.py         # Simulação de frete
  paint_estimator.py       # Cálculo de tinta
  ingest_csv.py            # Ingestão de produtos
```

**Estrutura sugerida para o agente**:
```
/app
  /api
    /webhooks
      whatsapp.py
    /endpoints
      health.py
      metrics.py
  /agents
    bertao.py
  /services
    product_search.py      # Integrar com api-produtos
    cart_manager.py
    payment.py
```

---

### 6. **Integração WhatsApp**

#### **Evolution API** ou **Baileys** (Recomendado)
- ✅ Open source
- ✅ Suporte completo a WhatsApp Business
- ✅ Webhooks nativos
- ✅ Suporte a mídia

**Alternativas**:
- **Twilio WhatsApp API**: Managed service, mais caro
- **Meta WhatsApp Business API**: Oficial, requer aprovação
- **Wati.io / ChatAPI**: SaaS, fácil integração

**Biblioteca Python**:
- `whatsapp-api-client-python` ou `python-whatsapp-bot`

---

### 7. **Banco de Dados**

#### **✅ PostgreSQL 15+** (JÁ EM USO)
- ✅ Dados relacionais (produtos já no schema `rag`)
- ✅ Transações ACID
- ✅ JSONB para dados flexíveis
- ✅ Extensões úteis (pgvector ✅, pg_trgm ✅, unaccent)

**Schema atual (produtos)**:
```sql
-- Schema rag (já implementado)
rag.products (
  id, sku, name, description, codigo_barras,
  embedding (vector), created_at, updated_at
)
-- Funções: rag.search_vec, rag.search_ft, rag.find_by_code
```

**Schema sugerido (novo - para o agente)**:
```sql
-- Schema público (a criar)
- customers (id, phone, name, email, address, created_at)
- conversations (id, customer_id, status, metadata, created_at)
- messages (id, conversation_id, role, content, timestamp)
- carts (id, customer_id, items, status, created_at)
- orders (id, customer_id, cart_id, total, status, payment_link)
```

#### **Redis 7+** (Recomendado - A implementar)
- ✅ Cache de produtos e buscas
- ✅ Sessões conversacionais
- ✅ Rate limiting
- ✅ Pub/Sub para eventos

**Nota**: PostgreSQL + pgvector já cobre busca vetorial, não é necessário Qdrant separado.

---

### 8. **Processamento Multimodal**

#### **Vision Models**:
- **Claude 3.5 Sonnet**: Análise de imagens nativa
- **GPT-4 Vision**: Alternativa
- **Google Gemini Vision**: Boa opção

#### **Audio Processing**:
- **Whisper (OpenAI)**: Transcrição de áudio
- **AssemblyAI**: Alternativa managed

#### **PDF Processing**:
- **PyPDF2** ou **pdfplumber**: Extração de texto
- **Claude/GPT-4**: Análise de conteúdo

**Bibliotecas**:
```python
# Imagens
from PIL import Image
import base64

# Áudio
import whisper  # OpenAI Whisper

# PDF
import PyPDF2
```

---

### 9. **Integrações Externas**

#### **✅ Integrações Já Implementadas**:
- **✅ VTEX**: 
  - Busca de produtos por SKU/RefId
  - Simulação de frete (`/api/checkout/pub/orderForms/simulation`)
  - Conversão SKU → ProductId
  - Implementado em `vtex_client.py` e `vtex_shipping.py`

#### **APIs Necessárias (A implementar)**:
- **Cálculo de Frete Alternativo**: 
  - Correios API (fallback se VTEX falhar)
  - Melhor Envio
  - Frete Rápido
- **Pagamento**:
  - Stripe
  - Mercado Pago
  - Asaas
  - Pix direto
- **Estoque/Produtos**:
  - ✅ API interna Copafer (`fetch_cubo_produtos.py` já existe)
  - ERP (se houver)

**Biblioteca de Integração**:
- ✅ `requests` (já em uso)
- `httpx` (async HTTP client - recomendado para novo código)
- `aiohttp` (alternativa)

---

### 10. **Gerenciamento de Estado e Memória**

#### **LangGraph State Management** (Recomendado)
- ✅ Estado persistente entre turnos
- ✅ Checkpointing automático
- ✅ Recuperação de conversas

**Persistência**:
- **PostgreSQL**: Estado de longo prazo
- **Redis**: Estado de sessão (TTL)
- **LangGraph Checkpoints**: Estado de execução

---

### 11. **Análise de Sentimento e Escalonamento**

#### **Análise de Sentimento**:
- **LLM nativo**: Usar Claude/GPT para análise
- **VADER (NLTK)**: Fallback rápido
- **Transformers (Hugging Face)**: Modelos especializados

#### **Sistema de Escalonamento**:
- **Regras baseadas em sentimento**
- **Detecção de palavras-chave** (PJ, orçamento, etc.)
- **Threshold de confiança do agente**

---

### 12. **Observabilidade e Monitoramento**

#### **Logging**:
- **structlog**: Logging estruturado
- **Python logging**: Padrão

#### **Métricas**:
- **Prometheus**: Coleta de métricas
- **Grafana**: Visualização
- **Custom metrics**: Taxa de conversão, tempo de resposta, etc.

#### **Tracing**:
- **OpenTelemetry**: Instrumentação
- **LangSmith** (LangChain): Tracing de agentes

#### **Error Tracking**:
- **Sentry**: Monitoramento de erros
- **Rollbar**: Alternativa

---

### 13. **Testes**

#### **Testes Unitários**:
- **pytest**: Framework de testes
- **pytest-asyncio**: Testes assíncronos
- **pytest-mock**: Mocks

#### **Testes de Integração**:
- **pytest**: Testes end-to-end
- **Testcontainers**: Containers para testes

#### **Testes de Agente**:
- **LangSmith**: Testes de prompts e agentes
- **Arize Phoenix**: Evals de LLM

---

### 14. **Infraestrutura**

#### **✅ Containerização (JÁ IMPLEMENTADO)**:
- ✅ **Docker**: Dockerfile funcional em `api-produtos`
- **Docker Compose**: Recomendado para desenvolvimento local (a criar)

#### **✅ Deploy (JÁ IMPLEMENTADO)**:
- ✅ **Fly.io**: API de produtos já deployada
  - Configuração em `fly.toml`
  - Região: `gru` (São Paulo)
  - Health check em `/docs`

#### **Orquestração** (Produção - Futuro):
- **Kubernetes**: Escalabilidade (se necessário)
- **Fly.io**: Continuar usando (simples e eficiente)
- **AWS ECS / Google Cloud Run**: Alternativas managed

#### **CI/CD** (A implementar):
- **GitHub Actions**: Pipelines recomendado
- **GitLab CI**: Alternativa

#### **Cloud Provider**:
- **Fly.io**: ✅ Já em uso
- **AWS**: Amplo suporte (se migrar)
- **Google Cloud**: Boa para IA
- **Azure**: Integração com OpenAI

---

### 15. **Segurança**

#### **Autenticação**:
- **JWT**: Tokens de API
- **OAuth 2.0**: Se necessário

#### **Segurança de Dados**:
- **Criptografia**: Dados sensíveis
- **LGPD Compliance**: Conformidade
- **Secrets Management**: 
  - AWS Secrets Manager
  - HashiCorp Vault
  - Environment variables (dev)

#### **Rate Limiting**:
- **Redis**: Rate limiting
- **FastAPI-limiter**: Middleware

---

## 📦 Dependências Principais

### ✅ Dependências Já Instaladas (`api-produtos/search_products_api/requirements.txt`)
```txt
fastapi
uvicorn[standard]
psycopg2-binary          # PostgreSQL (síncrono)
python-dotenv
openai                   # Embeddings
cohere                   # (instalado mas não usado)
tiktoken
requests                 # HTTP client
pandas                   # Processamento CSV
tqdm
```

### 📦 Dependências Adicionais Necessárias para o Agente

```txt
# Core Framework (NOVO)
langgraph>=0.2.0
langchain>=0.3.0
langchain-anthropic>=0.2.0
langchain-openai>=0.2.0

# API (já tem FastAPI, adicionar async)
httpx>=0.27.0            # Async HTTP client
asyncpg>=0.29.0          # PostgreSQL async (melhor performance)
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0          # Migrations

# WhatsApp (NOVO)
whatsapp-api-client-python>=1.0.0

# Database (NOVO)
redis>=5.0.0             # Cache e sessões

# Vector & Embeddings (já tem OpenAI, considerar upgrade)
# openai>=1.40.0         # Já instalado
sentence-transformers>=2.3.0  # Para embeddings locais (opcional)

# Multimodal (NOVO)
Pillow>=10.3.0
openai-whisper>=20231117
PyPDF2>=3.0.0

# Utils (já tem python-dotenv, adicionar)
structlog>=24.1.0
python-json-logger>=2.0.7

# Testing (NOVO)
pytest>=8.2.0
pytest-asyncio>=0.23.0
pytest-mock>=3.14.0

# Monitoring (NOVO)
sentry-sdk>=2.10.0
prometheus-client>=0.20.0
```

**Nota**: `psycopg2-binary` pode ser mantido para compatibilidade, mas `asyncpg` é recomendado para novas implementações assíncronas.

---

## 🚀 Estrutura de Projeto

### ✅ Estrutura Atual (`api-produtos/search_products_api/`)
```
api-produtos/search_products_api/
├── api.py                    # ✅ FastAPI app principal
├── search_products.py        # ✅ Busca híbrida de produtos
├── vtex_client.py           # ✅ Cliente VTEX
├── vtex_shipping.py         # ✅ Simulação de frete
├── paint_estimator.py       # ✅ Cálculo de tinta
├── ingest_csv.py            # ✅ Ingestão de produtos
├── fetch_cubo_produtos.py   # ✅ API Copafer
├── requirements.txt         # ✅ Dependências
├── Dockerfile               # ✅ Container
├── fly.toml                 # ✅ Deploy Fly.io
└── docs/                    # ✅ Documentação
```

### 🚀 Estrutura Sugerida para o Agente Bertão

```
copafer_v2/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
│
├── api-produtos/            # ✅ JÁ EXISTE
│   └── search_products_api/
│       └── ... (manter como está)
│
├── app/                     # 🆕 NOVO - Agente Bertão
│   ├── __init__.py
│   ├── main.py              # FastAPI app do agente
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── bertao.py        # Agente principal
│   │   ├── graph.py         # LangGraph definition
│   │   └── nodes/           # Nodes do grafo
│   │       ├── search.py    # Integra com api-produtos
│   │       ├── cart.py
│   │       ├── checkout.py
│   │       └── escalation.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── webhooks.py  # WhatsApp webhooks
│   │   │   ├── health.py
│   │   │   └── metrics.py
│   │   └── middleware.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── whatsapp.py      # WhatsApp service
│   │   ├── product_search.py # Wrapper para api-produtos
│   │   ├── cart_manager.py  # Gerenciamento de carrinho
│   │   ├── payment.py       # Integração pagamento
│   │   ├── shipping.py      # Wrapper para vtex_shipping
│   │   ├── recommendation.py # Sistema de recomendações
│   │   └── escalation.py    # Escalonamento
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py      # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── state.py         # LangGraph state
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py      # DB connections
│   │   ├── migrations/      # Alembic migrations
│   │   └── repositories/    # Data access layer
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── embeddings.py    # Embedding utilities
│   │   ├── sentiment.py    # Análise de sentimento
│   │   ├── media.py         # Processamento de mídia
│   │   └── formatters.py    # Formatação de mensagens
│   │
│   └── config/
│       ├── __init__.py
│       ├── settings.py      # Configurações
│       └── logging.py        # Logging config
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/
│   ├── seed_data.py
│   └── migrate_embeddings.py
│
└── docs/
    ├── api.md
    └── architecture.md
```

**Nota**: O agente pode consumir a API de produtos via HTTP (microserviço) ou importar diretamente os módulos Python.

---

## 🔄 Fluxo de Dados Simplificado

```
1. WhatsApp → Webhook → FastAPI (app/main.py)
2. FastAPI → LangGraph Agent (agents/bertao.py)
3. Agent → Product Search Service → api-produtos/search_products_api
   └─→ PostgreSQL + pgvector (schema rag) → Busca híbrida
4. Agent → Shipping Service → vtex_shipping.py → VTEX API
5. Agent → PostgreSQL → Persiste estado (conversas, carrinho, pedidos)
6. Agent → Redis → Cache (sessões, produtos frequentes)
7. Agent → WhatsApp → Resposta
```

**Integração com API de Produtos**:
- **Opção 1 (Recomendada)**: HTTP client para `api-produtos` (microserviço)
- **Opção 2**: Import direto dos módulos Python (monorepo)

---

## 📊 Métricas e Observabilidade

### Métricas Principais:
- **Tempo de resposta**: Prometheus + Grafana
- **Taxa de conversão**: Custom metrics
- **Custo por conversa**: Tracking de tokens
- **Taxa de escalonamento**: Custom metrics
- **Satisfação**: NPS tracking

### Logging:
- **Estruturado**: JSON logs com structlog
- **Níveis**: DEBUG, INFO, WARNING, ERROR
- **Contexto**: Conversation ID, Customer ID, etc.

---

## 🎯 Próximos Passos de Implementação

### Fase 1: Setup Inicial (Semana 1-2)
1. ✅ Configurar ambiente Python (já feito)
2. ✅ Setup FastAPI básico (já feito em api-produtos)
3. 🔄 Integração WhatsApp (webhook) - **PRÓXIMO**
4. 🔄 Configurar Redis (cache e sessões)
5. 🔄 Setup LangGraph básico

### Fase 2: Core Agent (Semana 3-4)
1. 🔄 Implementar grafo do agente (LangGraph)
2. ✅ Busca de produtos (RAG) - **JÁ FUNCIONAL** (integrar com api-produtos)
3. 🔄 Gerenciamento de carrinho
4. 🔄 Processamento de mídia básico

### Fase 3: Integrações (Semana 5-6)
1. ✅ Integração frete - **JÁ FUNCIONAL** (vtex_shipping.py)
2. 🔄 Integração pagamento
3. 🔄 Sistema de escalonamento
4. 🔄 Análise de sentimento

### Fase 4: Refinamento (Semana 7-8)
1. 🔄 Sistema de recomendações
2. 🔄 Personalização
3. 🔄 Otimização de prompts
4. 🔄 Testes e validação

**Nota**: A API de produtos já está funcional e pode ser integrada imediatamente ao agente.

---

## 🔌 Integração com API de Produtos Existente

### Estratégia de Integração

A API de produtos em `api-produtos/search_products_api/` já está funcional e deployada. Duas opções para integração:

#### **Opção 1: Microserviço (Recomendado)**
Consumir a API via HTTP, mantendo serviços desacoplados:

```python
# app/services/product_search.py
import httpx

class ProductSearchService:
    def __init__(self, api_base_url: str = "https://search-products-api.fly.dev"):
        self.api_base_url = api_base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def search(self, query: str, k: int = 8):
        response = await self.client.post(
            f"{self.api_base_url}/search",
            json={"query": query}
        )
        return response.json()
    
    async def estimate_paint(self, **params):
        response = await self.client.post(
            f"{self.api_base_url}/paint/estimate",
            json=params
        )
        return response.json()
    
    async def simulate_shipping(self, items: list, postal_code: str):
        response = await self.client.post(
            f"{self.api_base_url}/shipping/simulate",
            json={
                "items": items,
                "postalCode": postal_code,
                "country": "BRA"
            }
        )
        return response.json()
```

**Vantagens**:
- ✅ Desacoplamento completo
- ✅ Escalabilidade independente
- ✅ Deploy separado
- ✅ Fácil de testar

#### **Opção 2: Import Direto (Monorepo)**
Importar módulos Python diretamente:

```python
# app/services/product_search.py
import sys
from pathlib import Path

# Adiciona api-produtos ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "api-produtos" / "search_products_api"))

from search_products import search_products
from vtex_shipping import simulate_shipping_for_skus, ItemInput
from paint_estimator import estimate_paint as estimate_paint_logic

class ProductSearchService:
    def search(self, query: str, k: int = 8):
        return search_products(query, k=k)
    
    def estimate_paint(self, **params):
        return estimate_paint_logic(**params)
    
    def simulate_shipping(self, items: list, postal_code: str):
        item_inputs = [ItemInput(sku=item["sku"], quantity=item["quantity"]) 
                       for item in items]
        return simulate_shipping_for_skus(
            items=item_inputs,
            postal_code=postal_code
        )
```

**Vantagens**:
- ✅ Sem latência de rede
- ✅ Mais simples (sem HTTP)
- ✅ Compartilha conexão DB

**Recomendação**: Começar com **Opção 2** (import direto) para MVP, migrar para **Opção 1** (HTTP) quando precisar escalar.

### Endpoints Disponíveis na API de Produtos

| Endpoint | Método | Descrição | Status |
|----------|--------|-----------|--------|
| `/search` | POST | Busca híbrida de produtos | ✅ Funcional |
| `/paint/estimate` | POST | Cálculo de tinta | ✅ Funcional |
| `/vtex/sku/{sku}/productId` | GET | Conversão SKU → ProductId | ✅ Funcional |
| `/shipping/simulate` | POST | Simulação de frete VTEX | ✅ Funcional |
| `/shipping/simulate/slas` | POST | SLAs de frete simplificados | ✅ Funcional |

### Variáveis de Ambiente Necessárias

A API de produtos espera estas variáveis (já configuradas):
```bash
# Database
DB_HOST=...
DB_PORT=5432
DB_USER=...
DB_PASSWORD=...
DB_NAME=...

# OpenAI
OPENAI_API_KEY=...
EMB_MODEL=text-embedding-3-small
EMB_DIM=1536

# VTEX
VTEX_APP_KEY=...
VTEX_APP_TOKEN=...
VTEX_ACCOUNT_HOST=copafer.myvtex.com
```

---

## 🔗 Recursos e Documentação

- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **LangChain**: https://python.langchain.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Qdrant**: https://qdrant.tech/
- **Context7 MCP**: Para documentação atualizada

---

## ✅ Checklist de Decisões Técnicas

### ✅ Já Implementado
- [x] Linguagem: Python 3.11+ ✅
- [x] API Framework: FastAPI ✅
- [x] Database Principal: PostgreSQL ✅
- [x] Vector Search: PostgreSQL + pgvector ✅
- [x] Embeddings: OpenAI ✅
- [x] Integração VTEX: ✅
- [x] Containerização: Docker ✅
- [x] Deploy: Fly.io ✅

### 🔄 A Implementar
- [ ] Framework de Agentes: LangGraph
- [ ] LLM Principal: Claude 3.5 Sonnet
- [ ] Cache: Redis
- [ ] WhatsApp: Evolution API ou Baileys
- [ ] Observabilidade: Prometheus + Grafana + Sentry
- [ ] Processamento Multimodal: Whisper, Vision
- [ ] Sistema de Recomendações
- [ ] Análise de Sentimento

---

**Versão**: 1.0  
**Data**: Janeiro 2025  
**Status**: Recomendação Inicial

