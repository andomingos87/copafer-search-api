# fetch_cubo_produtos.py

## O que faz?

Este script consulta a **API do Cubo** e retorna informações sobre o total de produtos disponíveis. É útil para verificar quantos produtos existem antes de fazer uma ingestão completa.

---

## Função Principal

### fetch_totals()

Faz uma requisição GET na API e retorna os totais.

```python
from fetch_cubo_produtos import fetch_totals

total, total_pages = fetch_totals("*")
print(f"Total de produtos: {total}")
print(f"Total de páginas: {total_pages}")
```

**Parâmetros**:
- `termo`: Termo de busca (padrão: "*" = todos)
- `timeout`: Timeout em segundos (padrão: 30)

**Retorno**: Tupla `(total, totalPages)` ou `(None, None)` em caso de erro.

---

## Uso via CLI

```bash
# Buscar totais de todos os produtos
python fetch_cubo_produtos.py

# Buscar totais com termo específico
python fetch_cubo_produtos.py "cimento"
```

**Saída**:
```json
{"total": 76720, "totalPages": 1535}
```

---

## Configuração

A chave de API pode ser configurada via variável de ambiente:

```
X_COPAFER_KEY=sua-chave
```

Existe um valor padrão embutido no código para facilitar testes.

---

## API Utilizada

**URL**: `https://copafer.fortiddns.com/api/v2/cubo/produtos`

**Headers**:
- `x-copafer-key`: Chave de autenticação
- `Accept`: application/json

**Query Params**:
- `termo`: Termo de busca

---

## Código de Saída (CLI)

| Código | Significado |
|--------|-------------|
| 0 | Sucesso (ambos os valores retornados) |
| 1 | Erro (algum valor é None) |

---

## Tratamento de Erros

- Erros HTTP são logados no stderr
- Respostas não-JSON são identificadas
- Timeout configurável para redes lentas

