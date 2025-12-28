"""Testes unitários para fetch_product_images (API Copafer)."""
import pytest
from unittest.mock import Mock, patch
import requests
from image_checker import fetch_product_images


@pytest.mark.unit
class TestFetchProductImages:
    """Testes para fetch_product_images."""

    @patch("image_checker.requests.get")
    def test_returns_ok_with_images(self, mock_get, copafer_response_with_images):
        """Resposta ok com images=[{"base64": "..."}] -> ok=True e lista filtrada."""
        mock_response = Mock()
        mock_response.json.return_value = copafer_response_with_images
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        assert result["ok"] is True
        assert len(result["images"]) == 3
        assert all("base64" in img for img in result["images"])
        assert result["error"] is None

    @patch("image_checker.requests.get")
    def test_returns_false_when_no_images(self, mock_get, copafer_response_no_images):
        """Resposta ok sem images ou images inválido -> ok=False."""
        mock_response = Mock()
        mock_response.json.return_value = copafer_response_no_images
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Nenhuma imagem encontrada" in result["error"]

    @patch("image_checker.requests.get")
    def test_returns_false_when_images_missing(self, mock_get):
        """Resposta ok sem campo images -> ok=False."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Nenhuma imagem encontrada" in result["error"]

    @patch("image_checker.requests.get")
    def test_returns_false_when_images_not_list(self, mock_get):
        """Resposta ok com images não sendo lista -> ok=False."""
        mock_response = Mock()
        mock_response.json.return_value = {"images": "not a list"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Nenhuma imagem encontrada" in result["error"]

    @patch("image_checker.requests.get")
    def test_filters_invalid_images(self, mock_get):
        """Filtra imagens sem base64 válido."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "images": [
                {"base64": "valid_base64"},
                {"invalid": "no base64"},
                {"base64": ""},  # base64 vazio
                {"base64": "another_valid_base64"},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        assert result["ok"] is True
        assert len(result["images"]) == 2
        assert result["images"][0]["base64"] == "valid_base64"
        assert result["images"][1]["base64"] == "another_valid_base64"

    @patch("image_checker.requests.get")
    def test_handles_http_error(self, mock_get):
        """HTTPError -> ok=False e mensagem de erro."""
        mock_get.side_effect = requests.HTTPError("404 Not Found")

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Erro HTTP" in result["error"]

    @patch("image_checker.requests.get")
    def test_handles_timeout(self, mock_get):
        """Timeout -> ok=False e mensagem de erro."""
        mock_get.side_effect = requests.Timeout("Request timeout")

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Erro ao buscar imagens" in result["error"]

    @patch("image_checker.requests.get")
    def test_handles_generic_exception(self, mock_get):
        """Exception genérica -> ok=False e mensagem de erro."""
        mock_get.side_effect = Exception("Generic error")

        result = fetch_product_images("12345")

        assert result["ok"] is False
        assert result["images"] == []
        assert "Erro ao buscar imagens" in result["error"]

    @patch("image_checker.requests.get")
    def test_calls_api_with_correct_params(self, mock_get):
        """Verifica que chama API com parâmetros corretos."""
        mock_response = Mock()
        mock_response.json.return_value = {"images": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_product_images("12345")

        mock_get.assert_called_once()
        call_args = mock_get.call_args
        # Verifica que foi chamado com timeout
        assert call_args[1]["timeout"] == 15
        # Verifica que params contém id
        assert call_args[1]["params"]["id"] == "12345"
        # Verifica que headers foram passados
        assert "headers" in call_args[1]

