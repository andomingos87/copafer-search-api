# paint_estimator.py

## O que faz?

Este módulo calcula a **quantidade de tinta necessária** para pintar uma área e determina a **melhor combinação de latas** para comprar.

---

## Funções Principais

### estimate_paint()

Função principal que calcula tudo de uma vez.

**Parâmetros**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| total_area_m2 | float | Área total a ser pintada (m²) |
| coverage_m2_per_liter | float | Rendimento da tinta (m² por litro por demão) |
| coats | int | Número de demãos (padrão: 1) |
| exclude_area_m2 | float | Área a descontar (portas/janelas) |
| can_sizes_liters | list | Tamanhos de lata disponíveis |

**Exemplo**:
```python
result = estimate_paint(
    total_area_m2=100,      # 100m² de parede
    coverage_m2_per_liter=10,  # Tinta rende 10m²/L
    coats=2,                # 2 demãos
    exclude_area_m2=8,      # 8m² de portas/janelas
)
```

**Retorno**:
```python
{
    "paintable_area_m2": 92,      # Área efetiva
    "coats": 2,                   # Demãos
    "coverage_m2_per_liter": 10,  # Rendimento
    "liters_needed": 18.4,        # Litros necessários
    "cans": {"18.0": 1, "0.9": 1}, # Latas a comprar
    "total_cans": 2,              # Total de latas
    "total_liters": 18.9,         # Litros comprados
    "waste_liters": 0.5           # Desperdício
}
```

---

### compute_cans()

Calcula a melhor combinação de latas usando um algoritmo **guloso (greedy)**.

**Como funciona**:
1. Ordena tamanhos de lata do maior para o menor
2. Usa o máximo de latas grandes possível
3. Completa o restante com latas menores

**Exemplo**:
```python
cans, total, waste = compute_cans(
    liters_needed=20,
    can_sizes=[18.0, 3.6, 0.9]
)
# cans = {18.0: 1, 3.6: 1}  → 21.6L
# waste = 1.6L
```

---

## Tamanhos de Lata Padrão

Por padrão, o sistema considera estas latas disponíveis:

| Tamanho | Uso Comum |
|---------|-----------|
| 18.0 L  | Galão grande (lata de 18L) |
| 3.6 L   | Galão médio |
| 2.5 L   | Lata intermediária |
| 0.9 L   | Lata pequena |
| 0.5 L   | Amostra/teste |

---

## Fórmula de Cálculo

```
Área Pintável = Área Total - Área Excluída
Litros Necessários = (Área Pintável × Demãos) ÷ Rendimento
```

---

## Uso pela API

Este módulo é chamado pelo endpoint `POST /paint/estimate` em `api.py`:

```http
POST /paint/estimate
Content-Type: application/json

{
    "total_area_m2": 100,
    "coverage_m2_per_liter": 10,
    "coats": 2
}
```

