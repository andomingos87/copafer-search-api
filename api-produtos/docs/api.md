# api.py

## O que faz?

Este é o **arquivo principal** da aplicação. Ele cria o servidor FastAPI e define todos os endpoints disponíveis para uso externo.

---

## Endpoints Disponíveis

### 1. POST /search

**Função**: Busca produtos no catálogo

**Entrada**:
```json
{
  "query": "cimento 50kg"
}
```

**Saída**:
```json
{
  "method": "hybrid",
  "confidence": 0.85,
  "results": [
    {
      "sku": "12345",
      "name": "Cimento CP-II 50kg",
      "codigo_barras": "7891234567890",
      "score": 0.85
    }
  ]
}
```

---

### 2. POST /paint/estimate

**Função**: Calcula quantidade de tinta necessária para pintar uma área

**Entrada**:
```json
{
  "total_area_m2": 100,
  "coverage_m2_per_liter": 10,
  "coats": 2,
  "exclude_area_m2": 5,
  "can_sizes_liters": [18.0, 3.6, 0.9]
}
```

**Saída**:
```json
{
  "paintable_area_m2": 95,
  "liters_needed": 19,
  "cans": {"18.0": 1, "3.6": 1},
  "total_cans": 2,
  "waste_liters": 2.6
}
```

---

### 3. GET /vtex/sku/{sku}/productId

**Função**: Obtém o `ProductId` da VTEX a partir de um SKU

**Exemplo**: `GET /vtex/sku/33375/productId`

**Saída**:
```json
{
  "sku": "33375",
  "found": true,
  "productId": 12345
}
```

---

### 4. POST /shipping/simulate

**Função**: Simula frete na VTEX para uma lista de SKUs

**Entrada**:
```json
{
  "items": [
    {"sku": "33375", "quantity": 2}
  ],
  "postalCode": "01310100",
  "country": "BRA"
}
```

---

### 5. POST /shipping/simulate/slas

**Função**: Similar ao anterior, mas retorna apenas `{id, price}` dos SLAs de frete

---

## Como Funciona?

1. **Importações**: O arquivo importa funções de outros módulos:
   - `search_products` para busca
   - `paint_estimator` para cálculo de tinta
   - `vtex_shipping` para integração VTEX

2. **Carrega Variáveis**: Lê configurações do arquivo `.env`

3. **Define Schemas**: Usa Pydantic para validar entrada das requisições

4. **Cria Rotas**: Cada endpoint chama a função especializada correspondente

---

## Como Executar

```bash
# Diretamente
python api.py

# Ou com uvicorn (recomendado)
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em `http://localhost:8000`

Documentação automática: `http://localhost:8000/docs`

