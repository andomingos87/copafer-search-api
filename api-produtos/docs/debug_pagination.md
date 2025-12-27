# debug_pagination.py

## O que faz?

Este script de **debug** verifica se a paginação da API do Cubo está funcionando corretamente. Testa páginas específicas e compara com o esperado.

---

## Funções

### debug_pagination()

Verifica:
1. Metadados da primeira página (total, totalPages, limit)
2. Testa páginas específicas (início, meio, fim)
3. Valida se o iterador está coletando todos os itens

### test_full_iteration_count()

Conta todos os itens usando o iterador completo (pode demorar).

---

## Uso via CLI

```bash
python debug_pagination.py
```

O script pergunta se deseja fazer o teste completo (que processa todas as páginas).

---

## Saída Esperada

```
Debugando paginação da API do Cubo...
============================================================
Metadados da primeira página:
  Total de páginas: 1535
  Total de itens: 76720
  Página atual: 1
  Limite por página: 50
  Itens na primeira página: 50

Testando páginas específicas:
  Página 1: 50 itens (API reporta página 1)
  Página 100: 50 itens (API reporta página 100)
  Página 500: 50 itens (API reporta página 500)
  Página 1535: 20 itens (API reporta página 1535)

Testando iterador completo (primeiras 5 páginas):
  Itens coletados pelo iterador: 250
  Esperado (5 páginas × 50): 250
```

---

## Páginas Testadas

| Página | Por quê |
|--------|---------|
| 1 | Primeira página (baseline) |
| 100 | Página do meio |
| 500 | Página intermediária |
| 1000 | Página avançada |
| totalPages-1 | Penúltima |
| totalPages | Última |

---

## Indicadores de Problema

- ⚠️ Página vazia quando deveria ter dados
- ❌ Erro ao acessar página
- Discrepância entre itens esperados e coletados

