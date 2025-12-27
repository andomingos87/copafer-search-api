# analyze_missing_skus.py

## O que faz?

Este script de **debug** analisa por que alguns produtos da API do Cubo não são importados durante a ingestão. Ele identifica produtos com SKU inválido ou vazio.

---

## Problema que Resolve

Durante a ingestão, produtos sem SKU válido são ignorados. Este script ajuda a entender:

- Quantos produtos têm SKU vazio
- Quantos produtos têm SKU que fica vazio após normalização (ex: só pontos)
- Qual a taxa de rejeição estimada

---

## Função Principal

### analyze_sku_issues()

```python
analyze_sku_issues(limit_pages=5)
```

Analisa as primeiras N páginas da API e gera um relatório.

---

## Uso via CLI

```bash
# Analisar primeiras 5 páginas
python analyze_missing_skus.py

# Analisar primeiras 10 páginas
python analyze_missing_skus.py 10
```

---

## Saída Esperada

```
Analisando primeiras 5 páginas da API do Cubo...
============================================================
Total de itens analisados: 250
SKUs válidos: 248
SKUs inválidos (rejeitados): 2
  - SKUs vazios/None: 1
  - SKUs só com pontos: 1

Taxa de rejeição: 0.8%
Estimativa de produtos perdidos no total: ~614

============================================================
Amostras de produtos com SKU vazio:
  1. Raw: None | Desc: Produto sem código
  
Amostras de produtos com SKU só pontos:
  1. Raw: '...' -> '...' | Desc: Outro produto
```

---

## O que é Verificado

| Condição | Resultado |
|----------|-----------|
| SKU é `None` | Rejeitado |
| SKU é string vazia | Rejeitado |
| SKU vira vazio após remover pontos | Rejeitado |
| SKU válido após normalização | Aceito |

---

## Dependências

Reutiliza funções do `ingest_api.py`:
- `iter_all_items()` - itera pelos produtos da API
- `map_item_to_row()` - aplica mesma lógica da ingestão
- `norm_str()` - normalização de strings

