# search_products.py

## O que faz?

Este arquivo contém a **lógica principal de busca** de produtos. Ele implementa uma busca "híbrida" que combina várias estratégias para encontrar os produtos mais relevantes.

---

## Estratégias de Busca

### 1. Busca Determinística (SKU/EAN)

Se a query for exatamente um SKU ou código de barras, retorna o produto diretamente.

**Exemplo**: Buscar "123456" encontra o produto com SKU 123456.

### 2. Busca Vetorial (Embeddings)

Usa embeddings da OpenAI para encontrar produtos semanticamente similares.

**Como funciona**:
1. Converte a query em um vetor (embedding)
2. Compara com os vetores dos produtos no banco
3. Retorna os mais próximos por distância coseno

**Bom para**: Buscas por significado, mesmo sem palavras exatas.

### 3. Busca Full-Text

Busca tradicional por palavras no texto usando índices do PostgreSQL.

**Bom para**: Encontrar palavras exatas ou variações.

### 4. Busca Trigram (pg_trgm)

Encontra textos similares mesmo com erros de digitação.

**Bom para**: Tolerância a typos, nomes parciais.

### 5. Busca por Keyword (ILIKE)

Busca direta por palavras-chave no nome e descrição.

**Bom para**: Termos simples como "cimento", "tinta".

---

## Fusão de Resultados

Os resultados de cada estratégia são combinados usando pesos configuráveis:

| Estratégia | Peso Padrão |
|------------|-------------|
| Vetorial   | 50% (alpha) |
| Full-text  | 30% (beta)  |
| Trigram    | 10% (gamma) |
| Keyword    | 10% (delta) |

O score final de cada produto é calculado combinando os scores de cada estratégia.

---

## Função Principal

```python
search_products(
    q: str,           # Query de busca
    k: int = 8,       # Quantidade de resultados
    k_vec: int = 50,  # Candidatos da busca vetorial
    k_ft: int = 30,   # Candidatos do full-text
    k_trgm: int = 15, # Candidatos do trigram
    k_kw: int = 50,   # Candidatos do keyword
    alpha: float = 0.50,  # Peso vetorial
    beta: float = 0.30,   # Peso full-text
    gamma: float = 0.10,  # Peso trigram
    delta: float = 0.10,  # Peso keyword
)
```

---

## Retorno

```json
{
  "method": "hybrid",
  "confidence": 0.85,
  "weights": {"vec": 0.5, "ft": 0.3, "trgm": 0.1, "kw": 0.1},
  "results": [
    {
      "sku": "12345",
      "name": "Produto X",
      "codigo_barras": "789...",
      "score": 0.85,
      "vec": 0.9,
      "ft": 0.8,
      "trgm": 0.5,
      "kw": 1.0
    }
  ]
}
```

---

## Uso via CLI

```bash
python search_products.py --q "cimento 50kg" --k 10
```

---

## Dependências

- **PostgreSQL** com schema `rag` e funções:
  - `rag.find_by_code()` - busca por SKU/EAN
  - `rag.search_vec()` - busca vetorial
  - `rag.search_ft()` - busca full-text
- **OpenAI** para gerar embeddings
- **pgvector** para busca vetorial
- **pg_trgm** para busca trigram (opcional)

