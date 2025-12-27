# vtex_client.py

## O que faz?

Este é um **cliente VTEX simples** para consultar informações de SKU via linha de comando ou como biblioteca. É uma versão mais básica do `vtex_shipping.py`.

---

## Função Principal

### get_sku_by_ref_id()

Consulta a API VTEX e retorna todos os dados de um SKU.

```python
from vtex_client import get_sku_by_ref_id

data = get_sku_by_ref_id("33375")
print(data)
```

**Retorno** (exemplo):
```json
{
  "Id": 12345,
  "ProductId": 67890,
  "NameComplete": "Produto Exemplo",
  "IsActive": true,
  "RefId": "33375"
}
```

---

## Uso via CLI

```bash
# Consultar um SKU
python vtex_client.py 33375

# Saída: JSON com dados completos do SKU
```

---

## Configuração

O cliente lê credenciais do arquivo `.env`:

```
VTEX_APP_TOKEN=seu-token
VTEX_APP_KEY=sua-chave
VTEX_ACCOUNT_HOST=copafer.myvtex.com  # opcional
```

---

## Diferença para vtex_shipping.py

| Aspecto | vtex_client.py | vtex_shipping.py |
|---------|---------------|------------------|
| Propósito | Consulta simples | Integração completa |
| Funcionalidades | Apenas busca SKU | Busca + Simulação frete |
| Interface | CLI + função | Apenas funções |
| Retorno | Dados completos | Dados processados |

---

## Tratamento de Erros

- Valida se `ref_id` foi fornecido
- Verifica se credenciais existem no `.env`
- Inclui corpo de erro em exceções HTTP para facilitar debug

---

## Código de Saída (CLI)

| Código | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Parâmetro faltando |
| 2 | Erro na requisição |

