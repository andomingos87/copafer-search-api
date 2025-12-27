# ingest_api.py

## O que faz?

Este arquivo importa produtos diretamente da **API do Cubo** para o banco de dados. É uma alternativa ao `ingest_csv.py` que busca os dados de uma API externa em vez de um arquivo CSV.

---

## Fluxo de Processamento

```
API Cubo → Paginação → Mapeamento → Embeddings → PostgreSQL
```

### 1. Paginação

A API do Cubo retorna dados paginados. Este script:
- Busca a primeira página para descobrir o total
- Itera por todas as páginas automaticamente
- Trata erros e faz retries em caso de falha

### 2. Mapeamento

Converte os campos da API para o formato do banco:

| Campo API | Campo Banco |
|-----------|-------------|
| codigo_produto | sku |
| descricao | name |
| descricao_tecnica | description |
| codigo_barras | codigo_barras |

### 3. Embeddings e Inserção

Reutiliza funções do `ingest_csv.py`:
- `build_product_text()` - monta texto para embedding
- `chunk_by_tokens()` - divide em chunks
- `upsert_product()` - insere/atualiza produto
- `insert_chunks()` - insere chunks com embeddings

---

## Parâmetros CLI

```bash
python ingest_api.py [opções]
```

| Opção | Padrão | Descrição |
|-------|--------|-----------|
| `--termo` | "*" | Termo de busca na API |
| `--page-size` | 50 | Itens por página |
| `--start-page` | 1 | Página inicial |
| `--limit-pages` | None | Limitar páginas (para testes) |
| `--dry-run` | False | Apenas simula, não grava |
| `--verbose`, `-v` | False | Mostra logs detalhados |

---

## Exemplos de Uso

```bash
# Ingerir tudo
python ingest_api.py --verbose

# Testar com 5 páginas
python ingest_api.py --limit-pages 5 --verbose

# Simulação sem gravar
python ingest_api.py --dry-run --limit-pages 10

# Continuar a partir da página 100
python ingest_api.py --start-page 100
```

---

## Configuração

Variáveis de ambiente necessárias no `.env`:

```
X_COPAFER_KEY=sua-chave-api
CUBO_API_URL=https://copafer.fortiddns.com/api/v2/cubo/produtos
```

---

## Retries e Tolerância a Falhas

- Erros HTTP 5xx fazem até 3 retries
- Backoff exponencial entre tentativas
- Commits parciais a cada 200 produtos

---

## Saída

```json
{
  "ok": true,
  "dry_run": false,
  "upserted_products": 76720,
  "inserted_chunks": 76720
}
```

