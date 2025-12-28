"""Testes unitários para o fluxo principal check_image_exists."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from image_checker import (
    check_image_exists,
    ImageCheckRequest,
    ImageCheckResponse,
    NO_IMAGE_CODE,
)


@pytest.mark.unit
class TestCheckImageExists:
    """Testes para check_image_exists - fluxo principal."""

    @patch("image_checker.get_cached_image")
    def test_cache_hit_base64(self, mock_get_cached):
        """Cache hit base64 -> imageExists=True."""
        mock_get_cached.return_value = "base64_image_data"

        result = check_image_exists("12345")

        assert result["imageExists"] is True
        assert result["IdProduto"] == "12345"

    @patch("image_checker.get_cached_image")
    def test_cache_hit_null_string(self, mock_get_cached):
        """Cache hit "null" -> imageExists=False."""
        mock_get_cached.return_value = "null"

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"

    @patch("image_checker.get_cached_image")
    def test_cache_hit_empty_string(self, mock_get_cached):
        """Cache hit string vazia -> imageExists=False."""
        mock_get_cached.return_value = ""

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"

    @patch("image_checker.set_cached_image")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_api_no_images(
        self, mock_get_cached, mock_fetch, mock_set_cached
    ):
        """Cache miss + API sem imagens -> imageExists=False e grava cache "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": False,
            "images": [],
            "error": "Nenhuma imagem encontrada"
        }
        mock_set_cached.return_value = True

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_once_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_api_with_images_ai_chooses_valid(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Cache miss + API com imagens + IA escolhe índice válido -> imageExists=True e grava base64."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": 1,
            "justification": "Good image",
            "error": None
        }
        # Primeira chamada (set) retorna True, segunda (get após set) retorna o base64
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, dummy_base64_images[1]]

        result = check_image_exists("12345")

        assert result["imageExists"] is True
        assert result["IdProduto"] == "12345"
        # Deve ter chamado set_cached_image com o base64 escolhido
        mock_set_cached.assert_called_with("12345", dummy_base64_images[1])

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_ai_returns_no_image_code(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Cache miss + IA retorna 932042349 -> imageExists=False e grava "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": NO_IMAGE_CODE,
            "justification": "Nenhuma adequada",
            "error": None
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_ai_fails(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """IA falha -> imageExists=False e grava "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": False,
            "best_image_index": None,
            "justification": None,
            "error": "Erro na chamada"
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_copafer_fails(
        self, mock_get_cached, mock_fetch, mock_set_cached
    ):
        """Copafer falha -> imageExists=False (grava cache negativo conforme doc)."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": False,
            "images": [],
            "error": "Erro HTTP: 500"
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        # Conforme implementação atual, grava cache negativo
        mock_set_cached.assert_called_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_invalid_index(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Índice inválido (fora do range) -> imageExists=False e grava "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        # Índice 10 quando só temos 3 imagens
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": 10,
            "justification": "Invalid",
            "error": None
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_negative_index(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Índice negativo -> imageExists=False e grava "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": -1,
            "justification": "Invalid",
            "error": None
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_with("12345", None)

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_none_index(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """best_image_index None -> imageExists=False e grava "null"."""
        mock_get_cached.return_value = None  # Sem cache
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": None,
            "justification": "No choice",
            "error": None
        }
        mock_set_cached.return_value = True
        mock_get_cached.side_effect = [None, "null"]

        result = check_image_exists("12345")

        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        mock_set_cached.assert_called_with("12345", None)


@pytest.mark.unit
class TestPydanticModels:
    """Testes mínimos dos modelos Pydantic."""

    def test_image_check_request(self):
        """Valida ImageCheckRequest."""
        request = ImageCheckRequest(produto_id="12345")
        assert request.produto_id == "12345"

    def test_image_check_response(self):
        """Valida ImageCheckResponse."""
        response = ImageCheckResponse(imageExists=True, IdProduto="12345")
        assert response.imageExists is True
        assert response.IdProduto == "12345"

    def test_image_check_response_false(self):
        """Valida ImageCheckResponse com imageExists=False."""
        response = ImageCheckResponse(imageExists=False, IdProduto="12345")
        assert response.imageExists is False
        assert response.IdProduto == "12345"

