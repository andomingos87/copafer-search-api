"""Fixtures comuns para testes do image_checker."""
import logging
import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List

# Configura logging para testes de integração
# Mostra logs de WARNING e acima por padrão
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Para ver logs DEBUG durante testes, use: pytest -v -s --log-cli-level=DEBUG


@pytest.fixture
def dummy_base64_image() -> str:
    """Retorna uma string base64 dummy (não é uma imagem real, apenas para testes)."""
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


@pytest.fixture
def dummy_base64_images() -> List[str]:
    """Retorna uma lista de strings base64 dummy."""
    return [
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==",
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAGA8jR9awAAAABJRU5ErkJggg==",
    ]


@pytest.fixture
def copafer_response_with_images(dummy_base64_images: List[str]) -> Dict[str, Any]:
    """Resposta mockada da API Copafer com imagens."""
    return {
        "images": [
            {"base64": dummy_base64_images[0]},
            {"base64": dummy_base64_images[1]},
            {"base64": dummy_base64_images[2]},
        ]
    }


@pytest.fixture
def copafer_response_no_images() -> Dict[str, Any]:
    """Resposta mockada da API Copafer sem imagens."""
    return {"images": []}


@pytest.fixture
def copafer_response_invalid() -> Dict[str, Any]:
    """Resposta mockada da API Copafer inválida."""
    return {"data": "invalid"}


@pytest.fixture
def openrouter_response_valid() -> Dict[str, Any]:
    """Resposta mockada do OpenRouter com índice válido."""
    return {
        "choices": [
            {
                "message": {
                    "content": '{"justification": "Imagem clara e profissional", "best_image_index": 0}'
                }
            }
        ]
    }


@pytest.fixture
def openrouter_response_no_image_code() -> Dict[str, Any]:
    """Resposta mockada do OpenRouter com código especial 932042349."""
    return {
        "choices": [
            {
                "message": {
                    "content": '{"justification": "Nenhuma imagem adequada", "best_image_index": 932042349}'
                }
            }
        ]
    }


@pytest.fixture
def openrouter_response_empty_choices() -> Dict[str, Any]:
    """Resposta mockada do OpenRouter sem choices."""
    return {"choices": []}


@pytest.fixture
def openrouter_response_empty_content() -> Dict[str, Any]:
    """Resposta mockada do OpenRouter com conteúdo vazio."""
    return {
        "choices": [
            {
                "message": {
                    "content": ""
                }
            }
        ]
    }


@pytest.fixture
def openrouter_response_invalid_json() -> Dict[str, Any]:
    """Resposta mockada do OpenRouter com JSON inválido."""
    return {
        "choices": [
            {
                "message": {
                    "content": "not a valid json"
                }
            }
        ]
    }


@pytest.fixture
def mock_redis_client():
    """Mock de cliente Redis."""
    mock_client = MagicMock()
    mock_client.ping.return_value = True
    return mock_client


@pytest.fixture
def mock_requests_get(monkeypatch):
    """Mock para requests.get."""
    mock_get = Mock()
    monkeypatch.setattr("image_checker.requests.get", mock_get)
    return mock_get


@pytest.fixture
def mock_requests_post(monkeypatch):
    """Mock para requests.post."""
    mock_post = Mock()
    monkeypatch.setattr("image_checker.requests.post", mock_post)
    return mock_post

