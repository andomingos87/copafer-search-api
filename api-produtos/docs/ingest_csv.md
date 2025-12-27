# ingest_csv.py

## O que faz?

Este arquivo é responsável por **importar produtos de um arquivo CSV** para o banco de dados PostgreSQL. Ele processa cada linha, gera embeddings e insere os dados no schema `rag`.

---

## Fluxo de Processamento

```
CSV → Leitura → Normalização → Chunking → Embeddings → PostgreSQL
```

### 1. Leitura do CSV

- Tenta diferentes encodings: UTF-8, UTF-8-BOM, CP1252
- Tenta diferentes separadores: `,` e `;`
- Modo tolerante: pula linhas problemáticas se necessário

### 2. Normalização

- Remove espaços extras
- Normaliza SKUs (remove pontos)
- Converte valores decimais no formato brasileiro (1.234,56)

### 3. Chunking

Divide textos longos em pedaços menores (máximo 800 tokens) para que os embeddings funcionem bem.

### 4. Geração de Embeddings

Usa a API da OpenAI para converter o texto de cada produto em um vetor numérico.

### 5. Inserção no Banco

- Faz upsert na tabela `rag.products`
- Insere chunks na tabela `rag.product_chunks`

---

## Colunas Esperadas no CSV

| Coluna | Obrigatória | Descrição |
|--------|-------------|-----------|
| codigo_produto | ✅ | SKU do produto |
| descricao | ✅ | Nome do produto |
| descricao_tecnica | | Descrição detalhada |
| codigo_barras | | EAN |
| tipo | | Categoria/tipo |
| um | | Unidade de medida |
| qtde_cx | | Quantidade por caixa |
| estoque | | Quantidade em estoque |

---

## Configuração Interna

No início do arquivo, existem constantes que podem ser ajustadas:

```python
CSV_PATH = "resumido_200.csv"  # Arquivo de entrada
LIMIT = None                   # Limitar quantidade (None = todos)
START = 5000                   # Linha inicial
COUNT = 1000                   # Quantidade a processar
```

---

## Como Executar

```bash
# Editar constantes no arquivo e executar:
python ingest_csv.py
```

---

## Relatório de Erros

Se houver linhas problemáticas no CSV, um arquivo `.bad_lines.txt` é gerado com detalhes.

---

## Tabelas do Banco

### rag.products
```sql
- id (serial)
- sku (unique)
- name
- description
- codigo_barras
- tipo
- um
- qtde_cx
- estoque
- raw (json com dados originais)
```

### rag.product_chunks
```sql
- id (serial)
- product_id (FK)
- chunk_no
- content (texto)
- embedding (vector)
```

