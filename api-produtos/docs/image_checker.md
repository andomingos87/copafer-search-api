# image_checker.py - Implementação Python

## Visão Geral

Este documento descreve como implementar a funcionalidade de verificação de imagem de produto em Python, substituindo o workflow N8N atual. A funcionalidade verifica se existe uma imagem adequada para um produto, utilizando cache Redis para otimização e inteligência artificial (OpenRouter/GPT-5) para selecionar a melhor imagem entre múltiplas opções.

## Estrutura do Módulo

O módulo `image_checker.py` seguirá os padrões do projeto:
- Separação de lógica em funções puras
- Uso de Pydantic para modelos de dados
- Configuração via variáveis de ambiente
- Tratamento de erros robusto
- Integração com Redis para cache

## Dependências Necessárias

Adicionar ao `requirements.txt`:

```
redis
openai  # já existe, mas pode precisar de atualização
```

## Configuração (.env)

Adicionar as seguintes variáveis de ambiente:

```env
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# API Copafer (busca de imagens)
COPAFER_API_BASE_URL=https://copafer.fortiddns.com/api/v2
COPAFER_AUTH_HEADER=X-Copafer-Auth
COPAFER_AUTH_TOKEN=seu-token-aqui

# OpenRouter (IA para seleção de imagem)
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_API_KEY=seu-bearer-token-aqui
OPENROUTER_MODEL=openai/gpt-5-chat

# Cache
IMAGE_CACHE_TTL=259200  # 3 dias em segundos
```

## Modelos Pydantic

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ImageCheckRequest(BaseModel):
    """Request para verificar se existe imagem adequada."""
    produto_id: str

class ImageCheckResponse(BaseModel):
    """Response da verificação de imagem."""
    imageExists: bool
    IdProduto: str
```

## Estrutura do Código

### 1. Configuração e Imports

```python
import os
import json
import re
from typing import Optional, List, Dict, Any
import requests
import redis
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

# Config Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Config API Copafer
COPAFER_API_BASE_URL = os.getenv("COPAFER_API_BASE_URL", "").strip()
COPAFER_AUTH_HEADER = os.getenv("COPAFER_AUTH_HEADER", "X-Copafer-Auth").strip()
COPAFER_AUTH_TOKEN = os.getenv("COPAFER_AUTH_TOKEN", "").strip()

# Config OpenRouter
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-5-chat").strip()

# Cache TTL
IMAGE_CACHE_TTL = int(os.getenv("IMAGE_CACHE_TTL", "259200"))  # 3 dias

# Código especial para "nenhuma imagem adequada"
NO_IMAGE_CODE = 932042349
```

### 2. Cliente Redis

```python
def get_redis_client() -> Optional[redis.Redis]:
    """Cria e retorna cliente Redis."""
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD if REDIS_PASSWORD else None,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        # Testa conexão
        client.ping()
        return client
    except Exception:
        return None

def get_cached_image(produto_id: str) -> Optional[str]:
    """Busca imagem em cache no Redis.
    
    Retorna:
        - str: base64 da imagem se encontrada
        - "null": string "null" se produto foi marcado como sem imagem
        - None: se não há cache
    """
    r = get_redis_client()
    if r is None:
        return None
    
    try:
        key = f"best_image_for_{produto_id}"
        value = r.get(key)
        return value
    except Exception:
        return None

def set_cached_image(produto_id: str, base64_value: Optional[str], ttl: int = IMAGE_CACHE_TTL) -> bool:
    """Armazena imagem no cache Redis.
    
    Args:
        produto_id: ID do produto
        base64_value: Base64 da imagem ou None para marcar como sem imagem
        ttl: Tempo de vida em segundos (padrão: 3 dias)
    
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    r = get_redis_client()
    if r is None:
        return False
    
    try:
        key = f"best_image_for_{produto_id}"
        value = base64_value if base64_value is not None else "null"
        r.setex(key, ttl, value)
        return True
    except Exception:
        return False
```

### 3. Busca de Imagens na API Copafer

```python
def fetch_product_images(produto_id: str) -> Dict[str, Any]:
    """Busca imagens do produto na API Copafer.
    
    Args:
        produto_id: ID do produto
    
    Returns:
        {
            "ok": bool,
            "images": List[Dict[str, str]],  # [{"base64": "..."}]
            "error": Optional[str]
        }
    """
    url = f"{COPAFER_API_BASE_URL}/cubo/produtos/imagem"
    headers = {
        "Accept": "application/json",
        COPAFER_AUTH_HEADER: COPAFER_AUTH_TOKEN,
    }
    params = {"id": produto_id}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        images = data.get("images", [])
        if not images or not isinstance(images, list):
            return {
                "ok": False,
                "images": [],
                "error": "Nenhuma imagem encontrada na resposta"
            }
        
        # Valida que cada imagem tem base64
        valid_images = []
        for img in images:
            if isinstance(img, dict) and img.get("base64"):
                valid_images.append({"base64": img["base64"]})
        
        return {
            "ok": True,
            "images": valid_images,
            "error": None
        }
    except requests.HTTPError as e:
        return {
            "ok": False,
            "images": [],
            "error": f"Erro HTTP: {e}"
        }
    except Exception as e:
        return {
            "ok": False,
            "images": [],
            "error": f"Erro ao buscar imagens: {e}"
        }
```

### 4. Preparação e Chamada ao OpenRouter

```python
def prepare_openrouter_payload(images: List[Dict[str, str]]) -> Dict[str, Any]:
    """Prepara payload para OpenRouter com todas as imagens.
    
    Args:
        images: Lista de imagens com base64
    
    Returns:
        Payload JSON para OpenRouter
    """
    # Instrução em português
    instruction = {
        "type": "text",
        "text": (
            "Qual dessas imagens lhe parece mais adequada para mostrar ao cliente "
            "que deseja ver uma imagem do produto? Isto é, qual delas se encaixa melhor "
            "como imagem de capa do produto? ATENÇÃO: Se caso nenhuma imagem for adequada, "
            "pois não é uma imagem para o cliente que quer ver o produto em detalhes, "
            "a foto não é profissional etc, retorne o número 932042349 em best_image_index"
        )
    }
    
    # Converte imagens para formato image_url
    image_urls = []
    for img in images:
        base64 = img.get("base64", "")
        # Remove quebras de linha
        base64_clean = re.sub(r'\r?\n|\r', '', base64)
        image_urls.append({
            "type": "image_url",
            "image_url": {
                "url": base64_clean
            }
        })
    
    # Monta conteúdo: instrução + imagens
    content = [instruction] + image_urls
    
    # Schema JSON strict
    json_schema = {
        "type": "object",
        "properties": {
            "justification": {
                "type": "string",
                "description": "Justificativa da escolha da imagem curta e objetiva"
            },
            "best_image_index": {
                "type": "number",
                "description": "Index (começando de 0) da imagem escolhida. Caso nenhuma seja escolhida, retorne 932042349"
            }
        },
        "required": ["justification", "best_image_index"],
        "additionalProperties": False
    }
    
    return {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "strict": True,
                "schema": json_schema
            }
        }
    }

def call_openrouter(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Chama OpenRouter para analisar imagens.
    
    Args:
        payload: Payload preparado por prepare_openrouter_payload
    
    Returns:
        {
            "ok": bool,
            "best_image_index": Optional[int],
            "justification": Optional[str],
            "error": Optional[str]
        }
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.post(
            OPENROUTER_API_URL,
            json=payload,
            headers=headers,
            timeout=60  # IA pode demorar mais
        )
        resp.raise_for_status()
        data = resp.json()
        
        # Extrai resposta do modelo
        choices = data.get("choices", [])
        if not choices:
            return {
                "ok": False,
                "best_image_index": None,
                "justification": None,
                "error": "Nenhuma escolha retornada pela API"
            }
        
        message_content = choices[0].get("message", {}).get("content", "")
        if not message_content:
            return {
                "ok": False,
                "best_image_index": None,
                "justification": None,
                "error": "Conteúdo da mensagem vazio"
            }
        
        # Parse JSON da resposta
        try:
            parsed = json.loads(message_content)
            best_index = parsed.get("best_image_index")
            justification = parsed.get("justification", "")
            
            return {
                "ok": True,
                "best_image_index": int(best_index) if best_index is not None else None,
                "justification": justification,
                "error": None
            }
        except json.JSONDecodeError as e:
            return {
                "ok": False,
                "best_image_index": None,
                "justification": None,
                "error": f"Erro ao parsear JSON da resposta: {e}"
            }
            
    except requests.HTTPError as e:
        return {
            "ok": False,
            "best_image_index": None,
            "justification": None,
            "error": f"Erro HTTP: {e}"
        }
    except Exception as e:
        return {
            "ok": False,
            "best_image_index": None,
            "justification": None,
            "error": f"Erro ao chamar OpenRouter: {e}"
        }
```

### 5. Função Principal

```python
def check_image_exists(produto_id: str) -> Dict[str, Any]:
    """Função principal que verifica se existe imagem adequada para o produto.
    
    Fluxo:
    1. Verifica cache Redis
    2. Se não houver cache, busca imagens na API
    3. Se houver imagens, analisa com IA
    4. Armazena resultado no cache
    5. Retorna resposta
    
    Args:
        produto_id: ID do produto
    
    Returns:
        {
            "imageExists": bool,
            "IdProduto": str
        }
    """
    # 1. Verifica cache
    cached = get_cached_image(produto_id)
    
    if cached is not None:
        # Há cache (pode ser base64 ou "null")
        image_exists = cached != "null" and cached != ""
        return {
            "imageExists": image_exists,
            "IdProduto": produto_id
        }
    
    # 2. Não há cache - busca imagens na API
    images_result = fetch_product_images(produto_id)
    
    if not images_result["ok"] or not images_result["images"]:
        # Não há imagens disponíveis
        set_cached_image(produto_id, None)  # Marca como null no cache
        return {
            "imageExists": False,
            "IdProduto": produto_id
        }
    
    images = images_result["images"]
    
    # 3. Prepara e chama OpenRouter
    payload = prepare_openrouter_payload(images)
    ai_result = call_openrouter(payload)
    
    if not ai_result["ok"]:
        # Erro na chamada de IA - marca como sem imagem por segurança
        set_cached_image(produto_id, None)
        return {
            "imageExists": False,
            "IdProduto": produto_id
        }
    
    best_index = ai_result["best_image_index"]
    
    # 4. Verifica se modelo escolheu uma imagem válida
    if best_index is None or best_index == NO_IMAGE_CODE:
        # Nenhuma imagem adequada
        set_cached_image(produto_id, None)
        return {
            "imageExists": False,
            "IdProduto": produto_id
        }
    
    # 5. Extrai base64 da imagem escolhida
    if best_index < 0 or best_index >= len(images):
        # Índice inválido
        set_cached_image(produto_id, None)
        return {
            "imageExists": False,
            "IdProduto": produto_id
        }
    
    chosen_image_base64 = images[best_index]["base64"]
    
    # 6. Armazena no cache
    set_cached_image(produto_id, chosen_image_base64)
    
    # 7. Retorna resposta (reprocessa cache para garantir consistência)
    cached_after = get_cached_image(produto_id)
    image_exists = cached_after is not None and cached_after != "null" and cached_after != ""
    
    return {
        "imageExists": image_exists,
        "IdProduto": produto_id
    }
```

## Integração no api.py

Adicionar ao `api.py`:

```python
from image_checker import ImageCheckRequest, ImageCheckResponse, check_image_exists

@app.post("/is-image-exists", response_model=ImageCheckResponse)
def is_image_exists(req: ImageCheckRequest):
    """Verifica se existe uma imagem adequada para o produto.
    
    Endpoint que substitui o workflow N8N de verificação de imagem.
    Utiliza cache Redis e IA (OpenRouter/GPT-5) para selecionar a melhor imagem.
    """
    result = check_image_exists(req.produto_id)
    return ImageCheckResponse(**result)
```

## Casos de Erro e Tratamento

### Redis Indisponível

**Comportamento:**
- Sistema continua funcionando normalmente, mas sem cache
- Cada requisição buscará imagens e processará com IA
- Performance será reduzida (sem cache hit), mas funcionalidade mantida

**Exemplo de Log:**
```
WARNING: Erro de conexão com Redis (ConnectionError): Connection refused
INFO: Continuando sem cache - performance pode ser reduzida
```

**Mitigação:**
- Verificar se Redis está rodando: `redis-cli ping`
- Verificar variáveis de ambiente: `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- Para produção, considerar Redis gerenciado (Upstash, AWS ElastiCache, etc.)

### API Copafer Indisponível

**Comportamento:**
- Retorna `imageExists: false`
- Não armazena resultado no cache (para permitir retry futuro)
- Log de erro é registrado

**Exemplo de Resposta:**
```json
{
  "imageExists": false,
  "IdProduto": "45250"
}
```

**Códigos de Erro Comuns:**
- `401 Unauthorized`: Token de autenticação inválido ou expirado
- `404 Not Found`: Produto não encontrado na API
- `500 Internal Server Error`: Erro no servidor da API Copafer
- `Timeout`: Requisição excedeu 15 segundos

**Mitigação:**
- Verificar `COPAFER_AUTH_TOKEN` no `.env`
- Verificar `COPAFER_API_BASE_URL` está correto
- Verificar conectividade de rede com a API
- Considerar implementar retry logic para erros temporários

### OpenRouter Indisponível

**Comportamento:**
- Retorna `imageExists: false`
- Marca como `null` no cache (para evitar retries desnecessários)
- Log de erro é registrado

**Exemplo de Resposta:**
```json
{
  "imageExists": false,
  "IdProduto": "45250"
}
```

**Códigos de Erro Comuns:**
- `401 Unauthorized`: API key inválida ou expirada
- `429 Too Many Requests`: Rate limit excedido
- `500 Internal Server Error`: Erro no servidor OpenRouter
- `Timeout`: Requisição excedeu 60 segundos (IA pode demorar)

**Mitigação:**
- Verificar `OPENROUTER_API_KEY` no `.env`
- Verificar rate limits da conta OpenRouter
- Considerar aumentar timeout se necessário
- Verificar se modelo `OPENROUTER_MODEL` está disponível

### Erros de Validação

#### Produto ID Inválido

**Comportamento:**
- Se `produto_id` for vazio ou None, retorna erro de validação
- FastAPI retorna `422 Unprocessable Entity`

**Exemplo de Request Inválido:**
```json
{
  "produto_id": ""
}
```

**Resposta:**
```json
{
  "detail": [
    {
      "loc": ["body", "produto_id"],
      "msg": "ensure this value has at least 1 character",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

#### Resposta da API em Formato Inesperado

**Comportamento:**
- Se API Copafer retornar formato diferente do esperado, trata como "sem imagens"
- Log de warning é registrado

**Exemplo:**
```
WARNING: Nenhuma imagem encontrada na resposta da API Copafer
```

### Timeouts

**Configuração:**
- Redis: 5 segundos (conexão e operações)
- API Copafer: 15 segundos
- OpenRouter: 60 segundos (IA pode demorar mais)

**Comportamento em Timeout:**
- Redis: Continua sem cache
- API Copafer: Retorna `imageExists: false`
- OpenRouter: Retorna `imageExists: false` e marca como `null` no cache

**Ajuste de Timeouts:**
Os timeouts são hardcoded no código. Para ajustar, modificar:
- `socket_connect_timeout` e `socket_timeout` em `get_redis_client()`
- `timeout` em `fetch_product_images()` (atualmente 15s)
- `timeout` em `call_openrouter()` (atualmente 60s)

## Exemplos de Uso

### Uso via API (FastAPI)

#### Exemplo 1: Verificar se produto tem imagem adequada

```bash
# Request
curl -X POST "http://localhost:8000/is-image-exists" \
  -H "Content-Type: application/json" \
  -d '{"produto_id": "45250"}'

# Response (sucesso com imagem)
{
  "imageExists": true,
  "IdProduto": "45250"
}

# Response (sem imagem adequada)
{
  "imageExists": false,
  "IdProduto": "45250"
}
```

#### Exemplo 2: Usando Python requests

```python
import requests

url = "http://localhost:8000/is-image-exists"
payload = {"produto_id": "45250"}

response = requests.post(url, json=payload)
result = response.json()

print(f"Produto {result['IdProduto']} tem imagem: {result['imageExists']}")
```

#### Exemplo 3: Usando JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/is-image-exists', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ produto_id: '45250' })
});

const result = await response.json();
console.log(`Produto ${result.IdProduto} tem imagem: ${result.imageExists}`);
```

### Uso Direto do Módulo Python

#### Exemplo 1: Verificação básica

```python
from image_checker import check_image_exists

# Verifica se produto tem imagem adequada
result = check_image_exists("45250")
print(result)
# Output: {"imageExists": True, "IdProduto": "45250"}
```

#### Exemplo 2: Teste de cache

```python
from image_checker import check_image_exists
import time

# Primeira chamada - processa (busca imagens, analisa com IA)
start = time.time()
result1 = check_image_exists("45250")
time1 = time.time() - start
print(f"Primeira chamada: {time1:.2f}s - {result1}")

# Segunda chamada - usa cache (muito mais rápida)
start = time.time()
result2 = check_image_exists("45250")
time2 = time.time() - start
print(f"Segunda chamada: {time2:.2f}s - {result2}")

# Resultados devem ser idênticos
assert result1 == result2
assert time2 < time1  # Cache deve ser mais rápido
```

#### Exemplo 3: Manipulação direta do cache

```python
from image_checker import get_cached_image, set_cached_image

# Armazena imagem no cache
produto_id = "45250"
base64_image = "iVBORw0KGgoAAAANSUhEUgAA..."
set_cached_image(produto_id, base64_image, ttl=3600)  # 1 hora

# Recupera do cache
cached = get_cached_image(produto_id)
print(f"Imagem em cache: {cached[:50]}...")  # Primeiros 50 caracteres

# Marca produto como sem imagem
set_cached_image("99999", None, ttl=3600)
cached_null = get_cached_image("99999")
assert cached_null == "null"
```

#### Exemplo 4: Busca de imagens diretamente

```python
from image_checker import fetch_product_images

# Busca imagens do produto na API Copafer
result = fetch_product_images("45250")

if result["ok"]:
    print(f"Encontradas {len(result['images'])} imagens")
    for i, img in enumerate(result["images"]):
        print(f"Imagem {i}: {len(img['base64'])} caracteres base64")
else:
    print(f"Erro: {result['error']}")
```

## Testes

### Teste Manual

```python
# Teste básico
from image_checker import check_image_exists

result = check_image_exists("45250")
print(result)
# Esperado: {"imageExists": True/False, "IdProduto": "45250"}

# Teste de cache
result1 = check_image_exists("45250")  # Primeira chamada - processa
result2 = check_image_exists("45250")  # Segunda chamada - usa cache
assert result1 == result2
```

### Teste de Cache Redis

```python
from image_checker import get_cached_image, set_cached_image

# Testa set
set_cached_image("test_123", "base64_abc", ttl=60)
cached = get_cached_image("test_123")
assert cached == "base64_abc"

# Testa null
set_cached_image("test_456", None, ttl=60)
cached_null = get_cached_image("test_456")
assert cached_null == "null"
```

## Migração do N8N

### Passos para Migração

1. **Implementar código Python** seguindo esta documentação
2. **Configurar variáveis de ambiente** no servidor
3. **Instalar dependências** (`redis` principalmente)
4. **Testar endpoint** `/is-image-exists` localmente
5. **Desabilitar workflow N8N** (não deletar imediatamente)
6. **Monitorar logs** por alguns dias
7. **Remover workflow N8N** após confirmação de funcionamento

### Compatibilidade

- **Request**: Mesmo formato do N8N (`{"produto_id": "..."}`)
- **Response**: Mesmo formato do N8N (`{"imageExists": bool, "IdProduto": str}`)
- **Cache**: Mesma chave Redis (`best_image_for_{{ produto_id }}`)
- **TTL**: Mesmo valor (3 dias)

## Monitoramento

### Métricas Importantes

- Taxa de cache hit/miss
- Tempo de resposta (com e sem cache)
- Taxa de erro nas APIs externas
- Uso de memória Redis

### Logs Recomendados

```python
import logging

logger = logging.getLogger(__name__)

# No check_image_exists, adicionar logs:
logger.info(f"Verificando imagem para produto {produto_id}")
logger.debug(f"Cache hit: {cached is not None}")
logger.warning(f"Erro ao buscar imagens: {error}")
```

## Otimizações Futuras

1. **Batch processing**: Processar múltiplos produtos de uma vez
2. **Retry logic**: Retry automático em caso de falhas temporárias
3. **Circuit breaker**: Evitar chamadas excessivas a APIs indisponíveis
4. **Métricas**: Integração com sistema de métricas (Prometheus, etc.)
5. **Async**: Migrar para FastAPI async para melhor performance

## Troubleshooting

### Problema: Redis não conecta

**Sintomas:**
- Logs mostram "Erro de conexão com Redis"
- Sistema funciona mas sem cache (performance reduzida)

**Soluções:**

1. **Verificar se Redis está rodando:**
   ```bash
   redis-cli ping
   # Deve retornar: PONG
   ```

2. **Verificar variáveis de ambiente:**
   ```bash
   echo $REDIS_HOST
   echo $REDIS_PORT
   echo $REDIS_PASSWORD
   ```

3. **Testar conexão manualmente:**
   ```python
   import redis
   r = redis.Redis(host='localhost', port=6379, decode_responses=True)
   r.ping()  # Deve funcionar sem erro
   ```

4. **Para Redis com SSL (Upstash, etc.):**
   ```env
   REDIS_SSL=true
   REDIS_HOST=seu-host.upstash.io
   REDIS_PORT=6379
   REDIS_PASSWORD=seu-token
   ```

### Problema: API Copafer retorna 401

**Sintomas:**
- Erro "Erro HTTP: 401 Client Error: Unauthorized"
- Resposta sempre `imageExists: false`

**Soluções:**

1. **Verificar token no `.env`:**
   ```env
   COPAFER_AUTH_TOKEN=seu-token-correto
   COPAFER_AUTH_HEADER=X-Copafer-Auth
   ```

2. **Testar token manualmente:**
   ```bash
   curl -H "X-Copafer-Auth: seu-token" \
        "https://copafer.fortiddns.com/api/v2/cubo/produtos/imagem?id=45250"
   ```

3. **Verificar se token não expirou**

### Problema: OpenRouter retorna 401 ou 429

**Sintomas:**
- Erro "Erro HTTP: 401" ou "429 Too Many Requests"
- Resposta sempre `imageExists: false`

**Soluções:**

1. **Verificar API key:**
   ```env
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

2. **Verificar rate limits:**
   - Acessar dashboard OpenRouter
   - Verificar se não excedeu limites de requisições

3. **Verificar modelo disponível:**
   ```env
   OPENROUTER_MODEL=openai/gpt-5-chat
   ```
   - Alguns modelos podem não estar disponíveis
   - Verificar documentação OpenRouter para modelos alternativos

### Problema: Respostas muito lentas

**Sintomas:**
- Requisições demoram mais de 5 segundos
- Cache não está sendo usado

**Soluções:**

1. **Verificar se cache está funcionando:**
   ```python
   from image_checker import get_cached_image
   cached = get_cached_image("45250")
   print(f"Cache: {cached is not None}")
   ```

2. **Verificar logs para cache hits:**
   - Procurar por "Cache hit" nos logs
   - Se não aparecer, Redis pode não estar funcionando

3. **Otimizar TTL se necessário:**
   ```env
   IMAGE_CACHE_TTL=259200  # 3 dias (padrão)
   ```

### Problema: Imagens sempre retornam `false`

**Sintomas:**
- Mesmo produtos com imagens retornam `imageExists: false`
- IA pode estar rejeitando todas as imagens

**Soluções:**

1. **Verificar se imagens estão sendo encontradas:**
   ```python
   from image_checker import fetch_product_images
   result = fetch_product_images("45250")
   print(f"Imagens encontradas: {len(result['images'])}")
   ```

2. **Verificar resposta da IA:**
   - Adicionar logs temporários em `call_openrouter()`
   - Verificar se `best_image_index` está sendo retornado corretamente

3. **Verificar código especial:**
   - Se IA retornar `932042349`, significa que nenhuma imagem foi considerada adequada
   - Isso é comportamento esperado se imagens não são profissionais

### Problema: Cache não persiste entre reinicializações

**Sintomas:**
- Cache funciona durante execução
- Após reiniciar servidor, cache é perdido

**Soluções:**

1. **Verificar se Redis está persistindo dados:**
   ```bash
   redis-cli CONFIG GET save
   ```

2. **Para desenvolvimento local, isso é normal:**
   - Redis em memória pode perder dados ao reiniciar
   - Para produção, usar Redis persistente ou gerenciado

### Debug Avançado

**Habilitar logs detalhados:**

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Agora image_checker.py vai logar operações detalhadas
from image_checker import check_image_exists
result = check_image_exists("45250")
```

**Verificar chaves Redis manualmente:**
```bash
redis-cli
> KEYS best_image_for_*
> GET best_image_for_45250
> TTL best_image_for_45250
```

**Testar componentes isoladamente:**
```python
# Testar apenas Redis
from image_checker import get_redis_client
r = get_redis_client()
print(f"Redis conectado: {r is not None}")

# Testar apenas busca de imagens
from image_checker import fetch_product_images
result = fetch_product_images("45250")
print(f"Resultado: {result}")

# Testar apenas OpenRouter (requer imagens válidas)
from image_checker import prepare_openrouter_payload, call_openrouter
images = [{"base64": "..."}]  # Imagem base64 válida
payload = prepare_openrouter_payload(images)
result = call_openrouter(payload)
print(f"IA resultado: {result}")
```

## Notas de Implementação

- O código especial `932042349` é mantido para compatibilidade
- Cache armazena string `"null"` quando não há imagem (não None)
- Base64 é limpo (remove quebras de linha) antes de enviar para OpenRouter
- Validação de índices para evitar IndexError
- Timeouts configuráveis via variáveis de ambiente
- Suporte a Redis com SSL (para Upstash e outros serviços gerenciados)

