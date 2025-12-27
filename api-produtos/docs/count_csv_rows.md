# count_csv_rows.py

## O que faz?

Este script **conta o número de registros** em um arquivo CSV, respeitando corretamente campos com quebras de linha e aspas. É útil para validar a integridade de um CSV antes de processá-lo.

---

## Função Principal

### count_csv_rows()

Conta registros de um CSV de forma precisa.

```python
from count_csv_rows import count_csv_rows
from pathlib import Path

total, dados, cabecalho = count_csv_rows(
    Path("produtos.csv"),
    delimiter=";",
    quotechar='"',
    has_header=True
)

print(f"Total de linhas: {total}")
print(f"Registros de dados: {dados}")
print(f"Linhas de cabeçalho: {cabecalho}")
```

**Retorno**: Tupla `(total_linhas, registros_dados, linhas_cabecalho)`

---

## Configuração

No início do arquivo:

```python
INPUT_FILE = "./documents/produtos-cubo.csv"
DELIMITER = ";"
QUOTECHAR = '"'
HAS_HEADER = True
```

---

## Uso via CLI

```bash
python count_csv_rows.py
```

**Saída**:
```
Arquivo: ./documents/produtos-cubo.csv
Cabeçalho: 1
Registros (dados): 76720
Total de linhas (arquivo): 76721
```

---

## Por que não usar `wc -l`?

| Método | Campos com quebra de linha |
|--------|---------------------------|
| `wc -l` | ❌ Conta cada `\n` como linha |
| `count_csv_rows.py` | ✅ Conta registros lógicos |

**Exemplo**:
```csv
sku;descricao
123;"Produto com
descrição em
várias linhas"
456;"Produto normal"
```

- `wc -l` retorna: 5 linhas
- `count_csv_rows.py` retorna: 2 registros de dados + 1 cabeçalho

---

## Casos de Uso

1. **Validação antes da ingestão**: Verificar se o número de produtos no CSV bate com o esperado

2. **Debug de erros**: Quando a ingestão processa menos registros que o esperado

3. **Comparação**: Verificar se dois CSVs têm o mesmo número de registros

