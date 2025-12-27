# vtex_shipping.py

## O que faz?

Este módulo integra com a **plataforma VTEX** para simular frete e consultar informações de SKU. É usado pela API para oferecer funcionalidades de e-commerce.

---

## Funções Principais

### get_product_id_by_sku()

Consulta a VTEX e retorna o `ProductId` a partir de um SKU (RefId).

```python
product_id = get_product_id_by_sku("33375")
# Retorna: 12345 ou None se não encontrar
```

### simulate_shipping_for_skus()

Simula frete para uma lista de SKUs.

**Fluxo**:
1. Converte cada SKU para ProductId (via `get_product_id_by_sku`)
2. Monta payload para API VTEX
3. Chama endpoint de simulação
4. Retorna informações de frete

**Parâmetros**:
```python
simulate_shipping_for_skus(
    items=[ItemInput(sku="33375", quantity=2)],
    postal_code="01310100",
    country="BRA",
    sc="1"  # Sales Channel
)
```

**Retorno**:
```python
{
    "ok": True,
    "notFoundSkus": [],
    "request": {...},
    "logisticsInfo": [...],
    "slas": [
        {"itemIndex": 0, "slas": [{"id": "PAC", "price": 1500}]}
    ]
}
```

### extract_slas_id_price()

Extrai apenas `{id, price}` dos SLAs retornados.

```python
slas = extract_slas_id_price(logistics_info)
# Retorna: [{"id": "PAC", "price": 1500}, {"id": "Sedex", "price": 2500}]
```

---

## Models Pydantic

### ItemInput
```python
class ItemInput(BaseModel):
    sku: str
    quantity: int
    seller: str = "1"
```

### ShippingSimulateRequest
```python
class ShippingSimulateRequest(BaseModel):
    items: List[ItemInput]
    postalCode: str
    country: str = "BRA"
    sc: str = "1"
```

---

## Configuração

Variáveis de ambiente no `.env`:

```
VTEX_APP_KEY=sua-app-key
VTEX_APP_TOKEN=seu-app-token
VTEX_ACCOUNT_HOST=copafer.myvtex.com
```

---

## Endpoints VTEX Utilizados

| Endpoint | Método | Uso |
|----------|--------|-----|
| `/api/catalog/pvt/stockkeepingunit` | GET | Buscar SKU por RefId |
| `/api/checkout/pub/orderForms/simulation` | POST | Simular frete |

---

## Tratamento de Erros

- SKUs não encontrados são listados em `notFoundSkus`
- Erros HTTP retornam `ok: false` com mensagem
- Timeout de 15-20 segundos por requisição

