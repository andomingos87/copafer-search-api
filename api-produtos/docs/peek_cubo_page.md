# peek_cubo_page.py

## O que faz?

Este script faz uma requisição simples à API do Cubo e mostra a **estrutura da resposta**. É uma forma rápida de inspecionar o formato dos dados sem dependências extras.

---

## Diferença para debug_response_structure.py

| Aspecto | peek_cubo_page.py | debug_response_structure.py |
|---------|-------------------|----------------------------|
| Dependências | Apenas stdlib | Usa ingest_api |
| Complexidade | Simples | Mais completo |
| Uso | Inspeção rápida | Análise detalhada |

---

## Uso via CLI

```bash
python peek_cubo_page.py
```

---

## O que Mostra

1. **Top-level keys**: Lista de chaves na resposta
2. **Lista de itens**: Onde os produtos estão (ex: `produtos`, `items`, `data`)
3. **Campos do primeiro item**: Quais campos cada produto tem
4. **Primeiro item (resumo)**: Exemplo de um produto

---

## Saída Esperada

```
Top-level keys: ['total', 'totalPages', 'page', 'limit', 'produtos']
Lista de itens encontrada em 'produtos' com tamanho 50
Campos do primeiro item:
['codigo_produto', 'descricao', 'descricao_tecnica', 'codigo_barras', 'tipo', 'um', 'qtde_cx', 'estoque']
Primeiro item (resumo):
{"codigo_produto": "12345", "descricao": "CIMENTO CP-II 50KG", ...}
```

---

## Busca Inteligente de Itens

O script procura a lista de produtos em vários lugares:

1. `payload["items"]`
2. `payload["data"]`
3. `payload["produtos"]`
4. `payload["results"]`
5. `payload["content"]`
6. Campos aninhados (ex: `payload["data"]["items"]`)

Isso garante compatibilidade com diferentes formatos de API.

