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


# =====================
# Modelos Pydantic
# =====================

class ImageCheckRequest(BaseModel):
    """Request para verificar se existe imagem adequada."""
    produto_id: str


class ImageCheckResponse(BaseModel):
    """Response da verificação de imagem."""
    imageExists: bool
    IdProduto: str


# =====================
# Cliente Redis
# =====================

def get_redis_client() -> Optional[redis.Redis]:
    """Cria e retorna cliente Redis.
    
    Returns:
        Cliente Redis se conexão for bem-sucedida, None caso contrário.
    """
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
    
    Args:
        produto_id: ID do produto
        
    Returns:
        - str: base64 da imagem se encontrada
        - "null": string "null" se produto foi marcado como sem imagem
        - None: se não há cache ou erro
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


# =====================
# Busca de Imagens na API Copafer
# =====================

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


# =====================
# Integração OpenRouter
# =====================

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


# =====================
# Função Principal
# =====================

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

