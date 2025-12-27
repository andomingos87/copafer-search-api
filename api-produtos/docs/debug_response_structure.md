# debug_response_structure.py

## O que faz?

Este script de **debug** analisa a estrutura exata da resposta da API do Cubo. É útil quando a API muda e os dados param de ser extraídos corretamente.

---

## Função Principal

### analyze_response_structure()

Faz uma requisição e mostra:
1. Estrutura completa da resposta (primeiros 2000 chars)
2. Lista de chaves no nível raiz
3. Tipo e conteúdo de cada campo
4. Testa se a extração de itens funciona

---

## Uso via CLI

```bash
python debug_response_structure.py
```

---

## Saída Esperada

```
Analisando estrutura da resposta da API do Cubo...
============================================================
Estrutura completa da resposta:
{
  "total": 76720,
  "totalPages": 1535,
  "page": 1,
  "produtos": [
    {...}
  ]
}...

Chaves na resposta: ['total', 'totalPages', 'page', 'limit', 'produtos']

total: <class 'int'>
  Valor: 76720

totalPages: <class 'int'>
  Valor: 1535

produtos: <class 'list'>
  Lista com 50 itens
  Primeiro item tem chaves: ['codigo_produto', 'descricao', ...]...

============================================================
Testando extract_items com a função corrigida:
Primeiro item extraído: ['codigo_produto', 'descricao', ...]...
Itens extraídos da primeira página: 50
```

---

## Quando Usar

1. **API mudou**: Estrutura de resposta diferente do esperado
2. **Ingestão não funciona**: Nenhum item sendo extraído
3. **Debug de mapeamento**: Verificar campos disponíveis
4. **Documentação**: Entender formato da API

