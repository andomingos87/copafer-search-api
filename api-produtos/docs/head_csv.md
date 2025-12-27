# head_csv.py

## O que faz?

Este script extrai as **primeiras N linhas** de um arquivo CSV grande e salva em um novo arquivo menor. É útil para criar amostras de teste sem processar o arquivo inteiro.

---

## Configuração

As configurações são feitas diretamente no código:

```python
INPUT_FILE = "./documents/produtos-cubo.csv"  # Arquivo de entrada
COUNT = 200                                    # Quantidade de linhas
OUTPUT_FILE = "resumido_200.csv"              # Arquivo de saída
DELIMITER = ";"                                # Separador de colunas
QUOTECHAR = '"'                                # Caractere de aspas
INCLUDE_HEADER = True                          # Incluir cabeçalho
```

---

## Como Usar

1. Edite as configurações no início do arquivo
2. Execute:

```bash
python head_csv.py
```

**Saída**:
```
Criado: resumido_200.csv
```

---

## Comportamento

- **Preserva o cabeçalho** se `INCLUDE_HEADER = True`
- **Respeita campos com quebras de linha** usando o módulo `csv`
- **Ignora erros de encoding** usando `errors="ignore"`
- **Cria arquivo de saída** no mesmo diretório do script

---

## Exemplo de Uso Prático

Você tem um CSV com 76.000 produtos e quer testar a ingestão com apenas 200:

```python
# No head_csv.py:
INPUT_FILE = "produtos-cubo.csv"
COUNT = 200
OUTPUT_FILE = "teste_200.csv"
```

Depois:
```bash
python head_csv.py
# Gera: teste_200.csv com 200 produtos + cabeçalho
```

---

## Vantagens sobre `head` do terminal

| Aspecto | head_csv.py | head -n 200 |
|---------|-------------|-------------|
| Campos com quebra de linha | ✅ Trata corretamente | ❌ Pode cortar no meio |
| Encoding | Configurável | Depende do terminal |
| Delimitador | Configurável | Não se aplica |

