"""Testes unitários para funções OpenRouter do image_checker."""
import pytest
import json
from unittest.mock import Mock, patch
import requests
from image_checker import (
    prepare_openrouter_payload,
    call_openrouter,
    NO_IMAGE_CODE,
    OPENROUTER_MODEL,
)


@pytest.mark.unit
class TestPrepareOpenrouterPayload:
    """Testes para prepare_openrouter_payload."""

    def test_creates_correct_payload_structure(self, dummy_base64_images):
        """Verifica estrutura do payload."""
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)

        assert payload["model"] == OPENROUTER_MODEL
        assert "messages" in payload
        assert len(payload["messages"]) == 1
        assert payload["messages"][0]["role"] == "user"
        assert "content" in payload["messages"][0]

    def test_includes_instruction_text(self, dummy_base64_images):
        """Verifica que inclui instrução em português."""
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)

        content = payload["messages"][0]["content"]
        assert content[0]["type"] == "text"
        assert "imagem" in content[0]["text"].lower()
        assert str(NO_IMAGE_CODE) in content[0]["text"]

    def test_converts_images_to_image_url_format(self, dummy_base64_images):
        """Verifica conversão de imagens para formato image_url."""
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)

        content = payload["messages"][0]["content"]
        # Deve ter 1 instrução + 3 imagens
        assert len(content) == 4

        # Verifica formato das imagens
        for i in range(1, 4):
            assert content[i]["type"] == "image_url"
            assert "image_url" in content[i]
            assert "url" in content[i]["image_url"]

    def test_removes_line_breaks_from_base64(self, dummy_base64_images):
        """Verifica remoção de quebras de linha do base64."""
        base64_with_newlines = "base64\nwith\nnewlines\r\nhere"
        images = [{"base64": base64_with_newlines}]
        payload = prepare_openrouter_payload(images)

        content = payload["messages"][0]["content"]
        image_url = content[1]["image_url"]["url"]
        assert "\n" not in image_url
        assert "\r" not in image_url

    def test_includes_json_schema(self, dummy_base64_images):
        """Verifica que inclui schema JSON strict."""
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)

        assert "response_format" in payload
        assert payload["response_format"]["type"] == "json_schema"
        assert payload["response_format"]["json_schema"]["strict"] is True

        schema = payload["response_format"]["json_schema"]["schema"]
        assert "properties" in schema
        assert "best_image_index" in schema["properties"]
        assert "justification" in schema["properties"]
        assert schema["required"] == ["justification", "best_image_index"]
        assert schema["additionalProperties"] is False

    def test_handles_empty_images_list(self):
        """Lida com lista vazia de imagens."""
        payload = prepare_openrouter_payload([])

        content = payload["messages"][0]["content"]
        # Deve ter apenas a instrução
        assert len(content) == 1


@pytest.mark.unit
class TestCallOpenrouter:
    """Testes para call_openrouter."""

    @patch("image_checker.requests.post")
    def test_returns_ok_with_valid_response(self, mock_post, openrouter_response_valid):
        """Resposta ok com choices[0].message.content JSON válido -> parse correto."""
        mock_response = Mock()
        mock_response.json.return_value = openrouter_response_valid
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is True
        assert result["best_image_index"] == 0
        assert result["justification"] == "Imagem clara e profissional"
        assert result["error"] is None

    @patch("image_checker.requests.post")
    def test_returns_false_when_choices_empty(self, mock_post, openrouter_response_empty_choices):
        """Conteúdo vazio / choices vazio -> ok=False."""
        mock_response = Mock()
        mock_response.json.return_value = openrouter_response_empty_choices
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Nenhuma escolha retornada" in result["error"]

    @patch("image_checker.requests.post")
    def test_returns_false_when_content_empty(self, mock_post, openrouter_response_empty_content):
        """Conteúdo vazio -> ok=False."""
        mock_response = Mock()
        mock_response.json.return_value = openrouter_response_empty_content
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Conteúdo da mensagem vazio" in result["error"]

    @patch("image_checker.requests.post")
    def test_returns_false_when_json_invalid(self, mock_post, openrouter_response_invalid_json):
        """JSON inválido -> ok=False com erro de parse."""
        mock_response = Mock()
        mock_response.json.return_value = openrouter_response_invalid_json
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Erro ao parsear JSON" in result["error"]

    @patch("image_checker.requests.post")
    def test_handles_http_error(self, mock_post):
        """HTTPError -> ok=False."""
        mock_post.side_effect = requests.HTTPError("401 Unauthorized")

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Erro HTTP" in result["error"]

    @patch("image_checker.requests.post")
    def test_handles_timeout(self, mock_post):
        """Timeout -> ok=False."""
        mock_post.side_effect = requests.Timeout("Request timeout")

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Erro ao chamar OpenRouter" in result["error"]

    @patch("image_checker.requests.post")
    def test_handles_generic_exception(self, mock_post):
        """Exception genérica -> ok=False."""
        mock_post.side_effect = Exception("Generic error")

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is False
        assert result["best_image_index"] is None
        assert "Erro ao chamar OpenRouter" in result["error"]

    @patch("image_checker.requests.post")
    def test_parses_best_image_index_correctly(self, mock_post):
        """Parse correto do best_image_index."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"justification": "Test", "best_image_index": 2}'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is True
        assert result["best_image_index"] == 2

    @patch("image_checker.requests.post")
    def test_handles_no_image_code(self, mock_post, openrouter_response_no_image_code):
        """Lida com código especial 932042349."""
        mock_response = Mock()
        mock_response.json.return_value = openrouter_response_no_image_code
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        result = call_openrouter(payload)

        assert result["ok"] is True
        assert result["best_image_index"] == NO_IMAGE_CODE

    @patch("image_checker.requests.post")
    def test_uses_correct_headers(self, mock_post):
        """Verifica que usa headers corretos."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"justification": "Test", "best_image_index": 0}'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"model": "test", "messages": []}
        call_openrouter(payload)

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        # Verifica que headers foram passados
        assert "headers" in call_args[1]
        assert "Authorization" in call_args[1]["headers"]
        assert "Content-Type" in call_args[1]["headers"]
        assert call_args[1]["headers"]["Content-Type"] == "application/json"
        # Verifica timeout
        assert call_args[1]["timeout"] == 60

