# Workflow N8N: SE IMG EXISTE

## Visão Geral

Este workflow do N8N verifica se existe uma imagem adequada para um produto, utilizando cache Redis para otimização e inteligência artificial (OpenRouter/GPT-5) para selecionar a melhor imagem entre múltiplas opções disponíveis.

## Endpoint

- **Método**: POST
- **Path**: `/is-image-exists`
- **Webhook ID**: `146f06b5-9915-41d7-8e0b-2279f7db78bf`

## Fluxo de Execução

### 1. Webhook (Entrada)
**Tipo**: `n8n-nodes-base.webhook`

- Recebe uma requisição POST no endpoint `/is-image-exists`
- Espera um JSON no body com o campo `produto_id`
- Exemplo de payload:
```json
{
  "produto_id": "45250"
}
```

**Saída**: Dados da requisição HTTP (headers, body, params, query)

---

### 2. produto_id (Extração)
**Tipo**: `n8n-nodes-base.set`

- Extrai o `produto_id` do body da requisição
- Armazena em uma variável chamada `produto_id` para uso posterior
- Expressão: `={{ $json.body.produto_id }}`

**Saída**: Objeto com `produto_id`

---

### 3. Redis Verifica Base64 (Cache Check)
**Tipo**: `n8n-nodes-base.redis` (operação: `get`)

- Verifica se já existe uma imagem em cache no Redis para este produto
- Chave utilizada: `best_image_for_{{ produto_id }}`
- Se encontrar, retorna o valor armazenado (base64 da imagem ou `null`)
- Se não encontrar, retorna vazio

**Saída**: 
- Se existe: objeto com `propertyName` contendo o valor armazenado
- Se não existe: objeto com `propertyName` vazio

---

### 4. Base64 não armazenado? (Decisão de Cache)
**Tipo**: `n8n-nodes-base.if`

- Verifica se `propertyName` está vazio (ou seja, não há cache)
- **Condição**: `$json.propertyName` está vazio?

**Fluxos**:
- **TRUE (vazio)**: Não há cache → segue para buscar imagens na API
- **FALSE (não vazio)**: Há cache → segue para preparar resposta final

---

### 5. Call Imagens Produto (Busca de Imagens)
**Tipo**: `n8n-nodes-base.httpRequest` (GET)

- **URL**: `https://copafer.fortiddns.com/api/v2/cubo/produtos/imagem`
- **Método**: GET
- **Query Parameter**: `id={{ produto_id }}`
- **Autenticação**: HTTP Header Auth (credencial: "X-Copafer Auth")

- Busca todas as imagens disponíveis para o produto na API externa
- Retorna um array de imagens, cada uma com seu `base64`

**Saída**: Objeto com array `images[]`, onde cada item contém `base64`

---

### 6. Imagem Existe? (Validação de Imagens)
**Tipo**: `n8n-nodes-base.if`

- Verifica se existe pelo menos uma imagem no array retornado
- **Condição**: `$json.images[0].base64` existe?

**Fluxos**:
- **TRUE (existe)**: Há imagens → segue para análise com IA
- **FALSE (não existe)**: Não há imagens → marca produto como sem imagem

---

### 7. Code (Preparação para IA)
**Tipo**: `n8n-nodes-base.code` (JavaScript)

- Prepara o payload para envio ao OpenRouter (GPT-5)
- Converte todas as imagens base64 em formato adequado para a API de visão
- Cria uma instrução em português pedindo para escolher a melhor imagem
- Configura resposta estruturada em JSON com schema strict

**Lógica**:
1. Cria instrução de texto pedindo para escolher a imagem mais adequada como capa do produto
2. Converte todas as imagens base64 do array em objetos `image_url`
3. Remove quebras de linha dos base64
4. Monta o payload com:
   - Modelo: `openai/gpt-5-chat`
   - Mensagem com instrução + todas as imagens
   - Schema JSON strict com campos:
     - `justification`: Justificativa da escolha
     - `best_image_index`: Índice da imagem escolhida (ou `932042349` se nenhuma for adequada)

**Saída**: Payload JSON pronto para envio ao OpenRouter

---

### 8. OpenRouter Call (Análise com IA)
**Tipo**: `n8n-nodes-base.httpRequest` (POST)

- **URL**: `https://openrouter.ai/api/v1/chat/completions`
- **Método**: POST
- **Autenticação**: Bearer Token (credencial: "openrouter bearer")
- **Body**: Payload preparado pelo nó Code

- Envia todas as imagens para o GPT-5 analisar e escolher a melhor
- O modelo retorna um JSON com:
  - `justification`: Por que escolheu aquela imagem
  - `best_image_index`: Índice da imagem escolhida (0-based) ou `932042349` se nenhuma for adequada

**Saída**: Resposta da API com `choices[0].message.content` contendo JSON parseável

---

### 9. Edit Fields (Extração do Índice)
**Tipo**: `n8n-nodes-base.set`

- Extrai o `best_image_index` da resposta do OpenRouter
- Calcula `init` e `end` para usar no slice do array de imagens
- **Campos criados**:
  - `init`: `best_image_index` (índice inicial)
  - `end`: `best_image_index + 1` (índice final para slice)

**Saída**: Objeto com `init` e `end`

---

### 10. If (Validação de Imagem Adequada)
**Tipo**: `n8n-nodes-base.if`

- Verifica se o modelo escolheu uma imagem válida
- **Condição**: `$json.init` é diferente de `932042349`?

**Fluxos**:
- **TRUE (diferente de 932042349)**: Imagem adequada encontrada → extrai base64
- **FALSE (igual a 932042349)**: Nenhuma imagem adequada → marca como sem imagem

---

### 11. Edit Fields2 (Extração do Base64)
**Tipo**: `n8n-nodes-base.set`

- Extrai o base64 da imagem escolhida pelo modelo
- Busca no array de imagens do nó Code usando os índices `init` e `end`
- **Campo criado**:
  - `base64`: String base64 da melhor imagem

**Saída**: Objeto com `base64` da imagem escolhida

---

### 12. Redis Define Melhor Imagem (Cache da Imagem)
**Tipo**: `n8n-nodes-base.redis` (operação: `set`)

- Armazena a melhor imagem no Redis para cache futuro
- **Chave**: `best_image_for_{{ produto_id }}`
- **Valor**: Base64 da imagem escolhida (ou `null` se não houver)
- **TTL**: 259200 segundos (3 dias)

- Após salvar, retorna ao nó "Redis Verifica Base64" para reprocessar o fluxo e retornar a resposta

---

### 13. Redis Define Produto sem Imagem (Cache de Ausência)
**Tipo**: `n8n-nodes-base.redis` (operação: `set`)

- Armazena `null` no Redis quando não há imagem adequada
- **Chave**: `best_image_for_{{ produto_id }}`
- **Valor**: `null`
- **TTL**: 259200 segundos (3 dias)

- Usado quando:
  - Não há imagens disponíveis na API
  - O modelo determina que nenhuma imagem é adequada (retorna 932042349)

**Saída**: Nenhuma (nó final desta branch)

---

### 14. setDataProduct (Preparação de Resposta)
**Tipo**: `n8n-nodes-base.set`

- Prepara os dados finais para a resposta do webhook
- **Campos criados**:
  - `imageExists`: Boolean indicando se existe imagem (verifica se `propertyName !== "null"`)
  - `IdProduto`: String com o `produto_id`

- Executado quando há cache (não precisa buscar imagens novamente)

**Saída**: Objeto com `imageExists` e `IdProduto`

---

### 15. Respond to Webhook1 (Resposta Final)
**Tipo**: `n8n-nodes-base.respondToWebhook`

- Envia a resposta final para o cliente que fez a requisição
- Retorna os dados preparados pelo nó `setDataProduct`

**Resposta esperada**:
```json
{
  "imageExists": true,
  "IdProduto": "45250"
}
```

ou

```json
{
  "imageExists": false,
  "IdProduto": "45250"
}
```

---

## Diagrama de Fluxo

```
[Webhook] 
    ↓
[produto_id]
    ↓
[Redis Verifica Base64]
    ↓
[Base64 não armazenado?]
    ├─ TRUE → [Call Imagens Produto]
    │            ↓
    │        [Imagem Existe?]
    │            ├─ TRUE → [Code] → [OpenRouter Call] → [Edit Fields] → [If]
    │            │                                                          ├─ TRUE → [Edit Fields2] → [Redis Define Melhor Imagem] → [Redis Verifica Base64]
    │            │                                                          └─ FALSE → [Redis Define Produto sem Imagem]
    │            └─ FALSE → [Redis Define Produto sem Imagem]
    │
    └─ FALSE → [setDataProduct] → [Respond to Webhook1]
```

## Características Importantes

### Cache Redis
- **TTL**: 3 dias (259200 segundos)
- **Chave**: `best_image_for_{{ produto_id }}`
- **Valores possíveis**:
  - Base64 da imagem (string)
  - `null` (quando não há imagem adequada)

### Código Especial
- **932042349**: Código especial retornado pelo modelo quando nenhuma imagem é considerada adequada para exibição ao cliente

### Modelo de IA
- **Provedor**: OpenRouter
- **Modelo**: `openai/gpt-5-chat`
- **Função**: Análise visual para escolher a melhor imagem de capa do produto

### Autenticação
- **API Copafer**: HTTP Header Auth (credencial "X-Copafer Auth")
- **OpenRouter**: Bearer Token (credencial "openrouter bearer")

## Casos de Uso

1. **Primeira consulta (sem cache)**:
   - Busca imagens na API
   - Analisa com IA
   - Armazena resultado no Redis
   - Retorna resposta

2. **Consulta subsequente (com cache)**:
   - Verifica Redis
   - Retorna resultado imediatamente sem processar

3. **Produto sem imagens**:
   - Marca como `null` no cache
   - Retorna `imageExists: false`

4. **Nenhuma imagem adequada**:
   - Modelo retorna código especial 932042349
   - Marca como `null` no cache
   - Retorna `imageExists: false`

## Observações

- O workflow está ativo (`"active": true`)
- Tag: `TOOL`
- Execução em modo produção
- Há um nó desabilitado: "Redis Verifica Base" (linha 400) - parece ser um nó de teste

