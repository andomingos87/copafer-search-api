"""Testes de integração para image_checker.

Estes testes verificam o fluxo completo do image_checker com diferentes
configurações de serviços externos (Redis, API Copafer, OpenRouter).

IMPORTANTE: Estes testes podem requerer serviços externos configurados.
Use pytest markers para pular testes quando serviços não estiverem disponíveis.
"""
import pytest
import os
from unittest.mock import patch, Mock, MagicMock
from image_checker import (
    check_image_exists,
    get_redis_client,
    get_cached_image,
    set_cached_image,
    fetch_product_images,
    call_openrouter,
    prepare_openrouter_payload,
    IMAGE_CACHE_TTL,
    NO_IMAGE_CODE,
)


@pytest.mark.integration
class TestIntegrationRedis:
    """Testes de integração com Redis."""

    @pytest.mark.skipif(
        os.getenv("SKIP_REDIS_TESTS", "false").lower() == "true",
        reason="Redis tests skipped via SKIP_REDIS_TESTS env var"
    )
    def test_redis_connection_when_available(self):
        """Testa conexão com Redis quando disponível."""
        client = get_redis_client()
        if client is None:
            pytest.skip("Redis não está disponível")
        
        # Testa ping
        assert client.ping() is True

    @pytest.mark.skipif(
        os.getenv("SKIP_REDIS_TESTS", "false").lower() == "true",
        reason="Redis tests skipped via SKIP_REDIS_TESTS env var"
    )
    def test_cache_roundtrip(self):
        """Testa ciclo completo de cache: set -> get."""
        # Limpa cache antes do teste
        test_produto_id = "test_integration_12345"
        client = get_redis_client()
        if client is None:
            pytest.skip("Redis não está disponível")
        
        try:
            # Remove chave se existir
            client.delete(f"best_image_for_{test_produto_id}")
            
            # Testa set
            test_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            result_set = set_cached_image(test_produto_id, test_base64, ttl=60)
            assert result_set is True
            
            # Testa get
            result_get = get_cached_image(test_produto_id)
            assert result_get == test_base64
            
            # Testa set null
            result_set_null = set_cached_image(test_produto_id, None, ttl=60)
            assert result_set_null is True
            
            # Testa get null
            result_get_null = get_cached_image(test_produto_id)
            assert result_get_null == "null"
            
        finally:
            # Limpa após teste
            client.delete(f"best_image_for_{test_produto_id}")

    @pytest.mark.skipif(
        os.getenv("SKIP_REDIS_TESTS", "false").lower() == "true",
        reason="Redis tests skipped via SKIP_REDIS_TESTS env var"
    )
    def test_cache_ttl(self):
        """Testa que TTL está sendo aplicado corretamente."""
        test_produto_id = "test_ttl_12345"
        client = get_redis_client()
        if client is None:
            pytest.skip("Redis não está disponível")
        
        try:
            # Remove chave se existir
            client.delete(f"best_image_for_{test_produto_id}")
            
            # Grava com TTL curto
            test_base64 = "test_base64_data"
            set_cached_image(test_produto_id, test_base64, ttl=2)
            
            # Verifica que existe
            assert get_cached_image(test_produto_id) == test_base64
            
            # Verifica TTL no Redis
            ttl = client.ttl(f"best_image_for_{test_produto_id}")
            assert ttl > 0
            assert ttl <= 2
            
        finally:
            # Limpa após teste
            client.delete(f"best_image_for_{test_produto_id}")

    def test_cache_works_without_redis(self):
        """Testa que sistema continua funcionando sem Redis."""
        with patch("image_checker.get_redis_client", return_value=None):
            # Deve retornar None sem erro
            result = get_cached_image("test_id")
            assert result is None
            
            # Deve retornar False sem erro
            result_set = set_cached_image("test_id", "base64")
            assert result_set is False


@pytest.mark.integration
class TestIntegrationCopaferAPI:
    """Testes de integração com API Copafer."""

    @pytest.mark.skipif(
        os.getenv("SKIP_COPAFER_TESTS", "false").lower() == "true",
        reason="Copafer API tests skipped via SKIP_COPAFER_TESTS env var"
    )
    def test_fetch_product_images_with_real_api(self):
        """Testa busca de imagens com API real (se configurada)."""
        # Este teste requer API Copafer configurada
        produto_id = os.getenv("TEST_PRODUTO_ID", "45250")
        
        result = fetch_product_images(produto_id)
        
        # Verifica estrutura da resposta
        assert "ok" in result
        assert "images" in result
        assert "error" in result
        
        # Se ok=True, deve ter imagens válidas
        if result["ok"]:
            assert isinstance(result["images"], list)
            for img in result["images"]:
                assert isinstance(img, dict)
                assert "base64" in img

    def test_fetch_product_images_handles_api_unavailable(self):
        """Testa que sistema lida com API indisponível."""
        with patch("image_checker.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection error")
            
            result = fetch_product_images("12345")
            
            assert result["ok"] is False
            assert result["images"] == []
            assert result["error"] is not None


@pytest.mark.integration
class TestIntegrationOpenRouter:
    """Testes de integração com OpenRouter."""

    def test_prepare_payload_structure(self, dummy_base64_images):
        """Testa que payload preparado tem estrutura correta."""
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)
        
        # Verifica estrutura básica
        assert "model" in payload
        assert "messages" in payload
        assert len(payload["messages"]) == 1
        
        # Verifica content
        content = payload["messages"][0]["content"]
        assert len(content) == len(images) + 1  # 1 instrução + N imagens
        
        # Verifica schema JSON
        assert "response_format" in payload
        assert payload["response_format"]["type"] == "json_schema"
        assert payload["response_format"]["json_schema"]["strict"] is True

    @pytest.mark.skipif(
        os.getenv("SKIP_OPENROUTER_TESTS", "false").lower() == "true",
        reason="OpenRouter tests skipped via SKIP_OPENROUTER_TESTS env var"
    )
    def test_call_openrouter_with_real_api(self, dummy_base64_images):
        """Testa chamada real ao OpenRouter (se configurado)."""
        # Este teste requer OpenRouter configurado
        images = [{"base64": img} for img in dummy_base64_images]
        payload = prepare_openrouter_payload(images)
        
        result = call_openrouter(payload)
        
        # Verifica estrutura da resposta
        assert "ok" in result
        assert "best_image_index" in result
        assert "error" in result
        
        # Se ok=True, deve ter índice válido
        if result["ok"]:
            assert result["best_image_index"] is not None
            assert isinstance(result["best_image_index"], int)
            # Índice deve ser válido ou código especial
            assert (
                result["best_image_index"] == NO_IMAGE_CODE or
                0 <= result["best_image_index"] < len(images)
            )

    def test_call_openrouter_handles_api_unavailable(self):
        """Testa que sistema lida com OpenRouter indisponível."""
        payload = {"model": "test", "messages": []}
        
        with patch("image_checker.requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection error")
            
            result = call_openrouter(payload)
            
            assert result["ok"] is False
            assert result["best_image_index"] is None
            assert result["error"] is not None


@pytest.mark.integration
class TestIntegrationFullFlow:
    """Testes de integração do fluxo completo."""

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_full_flow_cache_miss_with_redis_available(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Testa fluxo completo com cache miss e Redis disponível."""
        # Simula cache miss
        mock_get_cached.side_effect = [None, dummy_base64_images[0]]
        
        # Simula API retornando imagens
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        
        # Simula preparação de payload
        mock_prepare.return_value = {"model": "test", "messages": []}
        
        # Simula IA escolhendo primeira imagem
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": 0,
            "justification": "Good image",
            "error": None
        }
        
        # Simula cache funcionando
        mock_set_cached.return_value = True
        
        result = check_image_exists("12345")
        
        # Verifica resultado
        assert result["imageExists"] is True
        assert result["IdProduto"] == "12345"
        
        # Verifica que cache foi chamado
        assert mock_set_cached.called
        mock_set_cached.assert_called_with("12345", dummy_base64_images[0])

    @patch("image_checker.set_cached_image")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_full_flow_cache_miss_without_redis(
        self,
        mock_get_cached,
        mock_fetch,
        mock_set_cached,
    ):
        """Testa fluxo completo com cache miss e Redis indisponível."""
        # Simula cache miss e Redis indisponível
        mock_get_cached.return_value = None
        mock_set_cached.return_value = False  # Redis indisponível
        
        # Simula API sem imagens
        mock_fetch.return_value = {
            "ok": False,
            "images": [],
            "error": "Nenhuma imagem encontrada"
        }
        
        result = check_image_exists("12345")
        
        # Sistema deve continuar funcionando
        assert result["imageExists"] is False
        assert result["IdProduto"] == "12345"
        
        # Tentou salvar no cache (mas falhou silenciosamente)
        assert mock_set_cached.called

    @patch("image_checker.get_cached_image")
    def test_full_flow_cache_hit(self, mock_get_cached):
        """Testa fluxo completo com cache hit."""
        # Simula cache hit com base64
        mock_get_cached.return_value = "base64_image_data"
        
        result = check_image_exists("12345")
        
        # Deve retornar imediatamente sem chamar APIs
        assert result["imageExists"] is True
        assert result["IdProduto"] == "12345"
        
        # Deve ter chamado get_cached_image apenas uma vez
        assert mock_get_cached.call_count == 1

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_full_flow_with_different_scenarios(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Testa diferentes cenários do fluxo completo."""
        scenarios = [
            {
                "name": "Produto sem imagens",
                "fetch_result": {"ok": False, "images": [], "error": "No images"},
                "expected_exists": False,
            },
            {
                "name": "IA retorna código especial",
                "fetch_result": {
                    "ok": True,
                    "images": [{"base64": img} for img in dummy_base64_images],
                    "error": None
                },
                "ai_result": {
                    "ok": True,
                    "best_image_index": NO_IMAGE_CODE,
                    "justification": "None adequate",
                    "error": None
                },
                "expected_exists": False,
            },
            {
                "name": "IA escolhe imagem válida",
                "fetch_result": {
                    "ok": True,
                    "images": [{"base64": img} for img in dummy_base64_images],
                    "error": None
                },
                "ai_result": {
                    "ok": True,
                    "best_image_index": 1,
                    "justification": "Good image",
                    "error": None
                },
                "expected_exists": True,
            },
        ]
        
        for scenario in scenarios:
            # Reset mocks
            mock_get_cached.reset_mock()
            mock_fetch.reset_mock()
            mock_prepare.reset_mock()
            mock_call_ai.reset_mock()
            mock_set_cached.reset_mock()
            
            # Setup mocks
            mock_get_cached.side_effect = [None, "base64" if scenario["expected_exists"] else "null"]
            mock_fetch.return_value = scenario["fetch_result"]
            
            if "ai_result" in scenario:
                mock_prepare.return_value = {"model": "test", "messages": []}
                mock_call_ai.return_value = scenario["ai_result"]
            
            mock_set_cached.return_value = True
            
            # Execute
            result = check_image_exists("12345")
            
            # Verify
            assert result["imageExists"] == scenario["expected_exists"], \
                f"Scenario '{scenario['name']}' failed"
            assert result["IdProduto"] == "12345"


@pytest.mark.integration
class TestIntegrationPerformance:
    """Testes de performance e comportamento do sistema."""

    @patch("image_checker.get_cached_image")
    def test_cache_hit_performance(self, mock_get_cached):
        """Testa que cache hit é rápido (não chama APIs externas)."""
        import time
        
        mock_get_cached.return_value = "base64_image_data"
        
        start = time.time()
        result = check_image_exists("12345")
        elapsed = time.time() - start
        
        # Cache hit deve ser muito rápido (< 100ms conforme critério)
        assert elapsed < 0.1, f"Cache hit demorou {elapsed:.3f}s, esperado < 0.1s"
        assert result["imageExists"] is True

    @patch("image_checker.set_cached_image")
    @patch("image_checker.call_openrouter")
    @patch("image_checker.prepare_openrouter_payload")
    @patch("image_checker.fetch_product_images")
    @patch("image_checker.get_cached_image")
    def test_cache_miss_does_not_block_on_redis_failure(
        self,
        mock_get_cached,
        mock_fetch,
        mock_prepare,
        mock_call_ai,
        mock_set_cached,
        dummy_base64_images,
    ):
        """Testa que falha no Redis não bloqueia o fluxo."""
        # Simula cache miss
        mock_get_cached.side_effect = [None, dummy_base64_images[0]]
        
        # Simula APIs funcionando
        mock_fetch.return_value = {
            "ok": True,
            "images": [{"base64": img} for img in dummy_base64_images],
            "error": None
        }
        mock_prepare.return_value = {"model": "test", "messages": []}
        mock_call_ai.return_value = {
            "ok": True,
            "best_image_index": 0,
            "justification": "Good",
            "error": None
        }
        
        # Simula Redis falhando no set
        mock_set_cached.return_value = False
        
        # Deve continuar funcionando mesmo com Redis falhando
        result = check_image_exists("12345")
        
        assert result["imageExists"] is True
        assert result["IdProduto"] == "12345"

