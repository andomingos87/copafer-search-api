# Projeto API – Descrição dos Arquivos

Este repositório contém utilitários e uma API (FastAPI) voltados à busca de produtos, ingestão de CSV, integração com VTEX e algumas ferramentas auxiliares.

## Descrição dos arquivos `.py`

- `api.py`
  - Serviço FastAPI com endpoints principais:
    - `POST /search`: busca produtos usando a função `search_products()`.
    - `POST /paint/estimate`: calcula estimativa de tinta (consome `paint_estimator.py`).
    - `GET /vtex/sku/{sku}/productId`: obtém `productId` na VTEX a partir do SKU/RefId.
    - `POST /shipping/simulate`: simula frete na VTEX para uma lista de SKUs.
    - `POST /shipping/simulate/slas`: retorna somente `{id, price}` de SLAs da simulação.
    - `POST /is-image-exists`: verifica se produto possui imagem adequada (consome `image_checker.py`).
  - Lê variáveis do `.env` local (em `api/.env`).
  - Executável com `uvicorn`.

- `search_products.py`
  - Função `search_products(query, k=8, ...)` que realiza busca híbrida no Postgres (schema `rag`):
    - Determinística por SKU/EAN (`rag.find_by_code`).
    - Vetorial (pgvector) com embeddings da OpenAI (`rag.search_vec`).
    - Full-text (`rag.search_ft`).
    - Opcionalmente trigram (`pg_trgm`) e reforço por palavra‑chave (ILIKE/unaccent).
  - Usa variáveis de banco via `.env` (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
  - Usa `OPENAI_API_KEY`, `EMB_MODEL` e `EMB_DIM` para embeddings.

- `ingest_csv.py`
  - Pipeline de ingestão de produtos a partir de CSV para o Postgres (schema `rag`).
  - Tarefas principais:
    - Leitura robusta de CSV (`pandas`) com diagnóstico e tolerância a linhas ruins.
    - Normalização de campos (SKU, nome, ean etc.).
    - Geração de texto para embedding e divisão em chunks por token.
    - Geração de embeddings (OpenAI) e inserção/upsert em tabelas (`rag.products`, etc.).
  - Configurável via `.env` e constantes internas (tamanho do lote, modelo de embedding, etc.).

- `paint_estimator.py`
  - Lógica pura para cálculo de tinta e composição de latas.
  - Funções:
    - `estimate_paint(...)`: calcula área pintável, litros necessários, decompõe em latas disponíveis e desperdício.
    - `compute_cans(...)`: algoritmo guloso para composição de latas.
  - Usado por `api.py` no endpoint `/paint/estimate`.

- `vtex_shipping.py`
  - Integração VTEX para simulação de frete e utilitários:
    - `ItemInput` e `ShippingSimulateRequest` (modelos Pydantic para requests).
    - `get_product_id_by_sku(ref_id)`: obtém `ProductId` a partir de um RefId (SKU) VTEX.
    - `simulate_shipping_for_skus(items, postal_code, ...)`: converte SKUs em `ProductId` e simula frete no endpoint de `orderForms/simulation`.
    - `extract_slas_id_price(logistics_info)`: extrai `{id, price}` de SLAs.
  - Lê credenciais do `.env` (`VTEX_APP_KEY`, `VTEX_APP_TOKEN`, `VTEX_ACCOUNT_HOST`).

- `vtex_client.py`
  - Cliente VTEX simples para consulta de SKU por `RefId` (via CLI ou função):
    - `get_sku_by_ref_id(ref_id, host=None)`: chama `/api/catalog/pvt/stockkeepingunit`.
  - Carrega `.env` local e/ou da raiz.
  - Uso via terminal: `python api/vtex_client.py <RefId>`.

- `fetch_cubo_produtos.py`
  - Faz `GET` em `https://copafer.fortiddns.com/api/v2/cubo/produtos` e retorna `total` e `totalPages`.
  - Permite informar `termo` de busca; lê `X_COPAFER_KEY` do ambiente (tem default de fallback).
  - Uso via terminal (imprime JSON com os totais e retorna código de status).

- `head_csv.py`
  - Gera um CSV de saída contendo o cabeçalho (se existir) e as primeiras `N` linhas de dados de um CSV de entrada.
  - Configurável: arquivo de entrada, quantidade, delimitador, aspas, etc.
  - Ex.: cria `resumido_200.csv` a partir de `documents/produtos-cubo.csv`.

- `count_csv_rows.py`
  - Conta linhas lógicas de um CSV respeitando delimitador/aspas.
  - Retorna total do arquivo, total de registros de dados e número de linhas de cabeçalho.
  - Útil para validar integridade do CSV antes da ingestão.

- `image_checker.py`
  - Verificação de imagem adequada para produtos utilizando cache Redis e IA (OpenRouter/GPT-5).
  - Função principal: `check_image_exists(produto_id)` que verifica se existe imagem adequada.
  - Utilizado por `api.py` no endpoint `/is-image-exists`.
  - Substitui workflow N8N `se_img_existe`.

## Observações

- Variáveis de ambiente são lidas do `.env` localizado neste diretório (`api/.env`). Exemplos relevantes:
  - Banco: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
  - OpenAI: `OPENAI_API_KEY`, `EMB_MODEL`, `EMB_DIM`.
  - VTEX: `VTEX_APP_KEY`, `VTEX_APP_TOKEN`, `VTEX_ACCOUNT_HOST`.
  - Cubo: `X_COPAFER_KEY`.
  - Redis (cache de imagens): `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`, `REDIS_SSL`.
  - OpenRouter (IA): `OPENROUTER_API_KEY`, `OPENROUTER_API_URL`, `OPENROUTER_MODEL`.
  - API Copafer (imagens): `COPAFER_API_BASE_URL`, `COPAFER_AUTH_HEADER`, `COPAFER_AUTH_TOKEN`.
  - Cache: `IMAGE_CACHE_TTL` (padrão: 259200 segundos = 3 dias).
- Requisitos de Python estão em `requirements.txt`.
- A API pode ser iniciada com: `uvicorn api:app --host 0.0.0.0 --port 8000` (na pasta `api/`).

## Exemplo de Uso: Verificação de Imagem

```bash
# Verificar se produto possui imagem adequada
curl -X POST "http://localhost:8000/is-image-exists" \
  -H "Content-Type: application/json" \
  -d '{"produto_id": "45250"}'

# Response
{
  "imageExists": true,
  "IdProduto": "45250"
}
```

Para mais detalhes, consulte `docs/image_checker.md`.
