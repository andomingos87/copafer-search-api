# test_pagination_bug.py

## O que faz?

Este script de **debug** identifica exatamente em qual página a paginação da API para de funcionar. Foi criado para investigar um bug onde nem todos os produtos eram ingeridos.

---

## Funções

### test_pagination_boundaries()

Testa páginas em "zonas críticas":
- Início (1-5)
- Área onde parou (~página 1170)
- Final (próximo a totalPages)

Para cada página mostra:
- ✓ Quantidade de itens se tiver dados
- ❌ Alerta se página vazia quando deveria ter dados

### test_continuous_iteration()

Usa o iterador completo e mostra onde exatamente ele para de retornar itens.

---

## Uso via CLI

```bash
python test_pagination_bug.py
```

---

## Saída Esperada

```
Testando limites de paginação...
============================================================
API reporta: 1535 páginas, 76720 itens totais

Testando páginas 1-5:
  Página 1: ✓ 50 itens
  Página 2: ✓ 50 itens
  ...

Testando páginas 1170-1179:
  Página 1170: ✓ 50 itens
  Página 1171: ✓ 50 itens
  ...

Testando páginas 1530-1535:
  Página 1530: ✓ 50 itens
  Página 1535: ✓ 20 itens

============================================================
Testando onde o iterador para...
  Página ~50: 2,500 itens coletados
  Página ~100: 5,000 itens coletados
  ...

Iterador parou em: 58,528 itens (~página 1170)
```

---

## Contexto do Bug

O problema investigado era:
- API reporta 76.720 produtos
- Ingestão processava apenas ~57.000
- ~19.000 produtos estavam sendo perdidos

Este script ajudou a identificar se o problema era:
1. ❌ Paginação da API parando
2. ❌ Iterador com bug
3. ✅ Produtos sem SKU válido sendo rejeitados

---

## Zonas de Teste

| Range | Por quê |
|-------|---------|
| 1-5 | Confirmar que início funciona |
| 1170-1179 | Onde 58.528 ÷ 50 = ~1170 (área de parada observada) |
| 1530-1535 | Final reportado pela API |

