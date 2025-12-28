"""Testes de compatibilidade com workflow N8N.

Estes testes validam que a implementação Python é compatível
com o workflow N8N `se_img_existe`, garantindo:
- Formato de request/response idêntico
- Chaves Redis no mesmo formato
- TTL de 3 dias
- Código especial 932042349
- Comportamento idêntico em todos os cenários
"""
import pytest
from unittest.mock import patch, Mock
from image_checker import (
    check_image_exists,
    get_cached_image,
    set_cached_image,
    ImageCheckRequest,
    ImageCheckResponse,
    IMAGE_CACHE_TTL,
    NO_IMAGE_CODE,
)


@pytest.mark.integration
class TestN8NCompatibility:
    """Testes de compatibilidade com workflow N8N."""

    def test_request_format_compatible(self):
        """Valida que formato de request é compatível com N8N."""
        # N8N espera: {"produto_id": "12345"}
        request = ImageCheckRequest(produto_id="12345")
        
        assert request.produto_id == "12345"
        assert isinstance(request.produto_id, str)

    def test_response_format_compatible(self):
        """Valida que formato de response é compatível com N8N."""
        # N8N retorna: {"imageExists": bool, "IdProduto": str}
        response_true = ImageCheckResponse(imageExists=True, IdProduto="12345")
        response_false = ImageCheckResponse(imageExists=False, IdProduto="12345")
        
        assert response_true.imageExists is True
        assert response_true.IdProduto == "12345"
        assert isinstance(response_true.imageExists, bool)
        assert isinstance(response_true.IdProduto, str)
        
        assert response_false.imageExists is False
        assert response_false.IdProduto == "12345"

    def test_redis_key_format_compatible(self):
        """Valida que chave Redis é idêntica ao N8N."""
        # N8N usa: best_image_for_{{ produto_id }}
        produto_id = "12345"
        expected_key = f"best_image_for_{produto_id}"
        
        with patch("image_checker.get_redis_client") as mock_get_client:
            mock_client = Mock()
            mock_client.get.return_value = "base64_data"
            mock_get_client.return_value = mock_client
            
            get_cached_image(produto_id)
            
            # Verifica que chave usada é a mesma do N8N
            mock_client.get.assert_called_once_with(expected_key)

    def test_redis_key_format_on_set(self):
        """Valida que chave Redis no set é idêntica ao N8N."""
        produto_id = "12345"
        expected_key = f"best_image_for_{produto_id}"
        
        with patch("image_checker.get_redis_client") as mock_get_client:
            mock_client = Mock()
            mock_client.setex.return_value = True
            mock_get_client.return_value = mock_client
            
            set_cached_image(produto_id, "base64_data")
            
            # Verifica que chave usada é a mesma do N8N
            mock_client.setex.assert_called_once()
            call_args = mock_client.setex.call_args[0]
            assert call_args[0] == expected_key

    def test_ttl_compatible_with_n8n(self):
        """Valida que TTL é de 3 dias (259200 segundos) como no N8N."""
        # N8N usa: 259200 segundos (3 dias)
        expected_ttl = 259200
        
        assert IMAGE_CACHE_TTL == expected_ttl, \
            f"TTL deve ser {expected_ttl} segundos (3 dias), mas é {IMAGE_CACHE_TTL}"

    def test_ttl_used_in_cache_set(self):
        """Valida que TTL é usado corretamente no set."""
        produto_id = "12345"
        
        with patch("image_checker.get_redis_client") as mock_get_client:
            mock_client = Mock()
            mock_client.setex.return_value = True
            mock_get_client.return_value = mock_client
            
            set_cached_image(produto_id, "base64_data")
            
            # Verifica que TTL usado é o padrão (3 dias)
            call_args = mock_client.setex.call_args[0]
            assert call_args[1] == IMAGE_CACHE_TTL

    def test_no_image_code_compatible(self):
        """Valida que código especial é 932042349 como no N8N."""
        # N8N usa: 932042349 quando nenhuma imagem é adequada
        expected_code = 932042349
        
        assert NO_IMAGE_CODE == expected_code, \
            f"Código especial deve ser {expected_code}, mas é {NO_IMAGE_CODE}"

    def test_null_string_in_cache_compatible(self):
        """Valida que string 'null' é usada no cache como no N8N."""
        # N8N armazena string "null" quando não há imagem
        produto_id = "12345"
        
        with patch("image_checker.get_redis_client") as mock_get_client:
            mock_client = Mock()
            mock_client.setex.return_value = True
            mock_get_client.return_value = mock_client
            
            set_cached_image(produto_id, None)
            
            # Verifica que valor armazenado é string "null"
            call_args = mock_client.setex.call_args[0]
            assert call_args[2] == "null"

    def test_cache_hit_base64_returns_true(self):
        """Valida que cache hit com base64 retorna imageExists=True."""
        # N8N: se propertyName !== "null" e não vazio -> imageExists=true
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = "base64_image_data"
            
            result = check_image_exists("12345")
            
            assert result["imageExists"] is True
            assert result["IdProduto"] == "12345"

    def test_cache_hit_null_returns_false(self):
        """Valida que cache hit com "null" retorna imageExists=False."""
        # N8N: se propertyName === "null" -> imageExists=false
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = "null"
            
            result = check_image_exists("12345")
            
            assert result["imageExists"] is False
            assert result["IdProduto"] == "12345"

    def test_cache_hit_empty_returns_false(self):
        """Valida que cache hit com string vazia retorna imageExists=False."""
        # N8N: se propertyName vazio -> imageExists=false
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = ""
            
            result = check_image_exists("12345")
            
            assert result["imageExists"] is False
            assert result["IdProduto"] == "12345"

    def test_no_images_sets_null_in_cache(self):
        """Valida que produto sem imagens grava "null" no cache."""
        # N8N: quando não há imagens, grava "null" no Redis
        with patch("image_checker.set_cached_image") as mock_set:
            with patch("image_checker.fetch_product_images") as mock_fetch:
                with patch("image_checker.get_cached_image") as mock_get:
                    mock_get.return_value = None  # Cache miss
                    mock_fetch.return_value = {
                        "ok": False,
                        "images": [],
                        "error": "Nenhuma imagem encontrada"
                    }
                    mock_set.return_value = True
                    
                    result = check_image_exists("12345")
                    
                    assert result["imageExists"] is False
                    # Deve ter tentado gravar "null" no cache
                    mock_set.assert_called_once_with("12345", None)

    def test_no_image_code_sets_null_in_cache(self):
        """Valida que código especial 932042349 grava "null" no cache."""
        # N8N: quando modelo retorna 932042349, grava "null" no Redis
        with patch("image_checker.set_cached_image") as mock_set:
            with patch("image_checker.call_openrouter") as mock_ai:
                with patch("image_checker.prepare_openrouter_payload") as mock_prepare:
                    with patch("image_checker.fetch_product_images") as mock_fetch:
                        with patch("image_checker.get_cached_image") as mock_get:
                            mock_get.return_value = None  # Cache miss
                            mock_fetch.return_value = {
                                "ok": True,
                                "images": [{"base64": "img1"}, {"base64": "img2"}],
                                "error": None
                            }
                            mock_prepare.return_value = {"model": "test", "messages": []}
                            mock_ai.return_value = {
                                "ok": True,
                                "best_image_index": NO_IMAGE_CODE,
                                "justification": "Nenhuma adequada",
                                "error": None
                            }
                            mock_set.return_value = True
                            
                            result = check_image_exists("12345")
                            
                            assert result["imageExists"] is False
                            # Deve ter tentado gravar "null" no cache
                            mock_set.assert_called_once_with("12345", None)

    def test_valid_image_sets_base64_in_cache(self):
        """Valida que imagem válida grava base64 no cache."""
        # N8N: quando modelo escolhe imagem válida, grava base64 no Redis
        test_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        with patch("image_checker.set_cached_image") as mock_set:
            with patch("image_checker.call_openrouter") as mock_ai:
                with patch("image_checker.prepare_openrouter_payload") as mock_prepare:
                    with patch("image_checker.fetch_product_images") as mock_fetch:
                        with patch("image_checker.get_cached_image") as mock_get:
                            mock_get.side_effect = [None, test_base64]  # Cache miss, depois hit
                            mock_fetch.return_value = {
                                "ok": True,
                                "images": [{"base64": test_base64}],
                                "error": None
                            }
                            mock_prepare.return_value = {"model": "test", "messages": []}
                            mock_ai.return_value = {
                                "ok": True,
                                "best_image_index": 0,
                                "justification": "Boa imagem",
                                "error": None
                            }
                            mock_set.return_value = True
                            
                            result = check_image_exists("12345")
                            
                            assert result["imageExists"] is True
                            # Deve ter tentado gravar base64 no cache
                            mock_set.assert_called_with("12345", test_base64)

    def test_response_structure_matches_n8n(self):
        """Valida que estrutura de resposta é idêntica ao N8N."""
        # N8N retorna: {"imageExists": bool, "IdProduto": str}
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = "base64_data"
            
            result = check_image_exists("12345")
            
            # Verifica estrutura exata
            assert "imageExists" in result
            assert "IdProduto" in result
            assert len(result) == 2  # Apenas estes dois campos
            
            # Verifica tipos
            assert isinstance(result["imageExists"], bool)
            assert isinstance(result["IdProduto"], str)

    def test_all_scenarios_match_n8n_behavior(self):
        """Valida que todos os cenários têm comportamento idêntico ao N8N."""
        scenarios = [
            {
                "name": "Cache hit com base64",
                "cache": "base64_data",
                "expected": {"imageExists": True, "IdProduto": "12345"},
            },
            {
                "name": "Cache hit com null",
                "cache": "null",
                "expected": {"imageExists": False, "IdProduto": "12345"},
            },
            {
                "name": "Cache hit com vazio",
                "cache": "",
                "expected": {"imageExists": False, "IdProduto": "12345"},
            },
            {
                "name": "Cache miss, sem imagens",
                "cache": None,
                "fetch": {"ok": False, "images": [], "error": "No images"},
                "expected": {"imageExists": False, "IdProduto": "12345"},
                "cache_set": None,  # Deve gravar null
            },
            {
                "name": "Cache miss, código especial",
                "cache": None,
                "fetch": {"ok": True, "images": [{"base64": "img1"}], "error": None},
                "ai": {"ok": True, "best_image_index": NO_IMAGE_CODE, "justification": "None", "error": None},
                "expected": {"imageExists": False, "IdProduto": "12345"},
                "cache_set": None,  # Deve gravar null
            },
            {
                "name": "Cache miss, imagem válida",
                "cache": None,
                "fetch": {"ok": True, "images": [{"base64": "img1"}], "error": None},
                "ai": {"ok": True, "best_image_index": 0, "justification": "Good", "error": None},
                "expected": {"imageExists": True, "IdProduto": "12345"},
                "cache_set": "img1",  # Deve gravar base64
            },
        ]
        
        for scenario in scenarios:
            with patch("image_checker.set_cached_image") as mock_set:
                with patch("image_checker.call_openrouter") as mock_ai:
                    with patch("image_checker.prepare_openrouter_payload") as mock_prepare:
                        with patch("image_checker.fetch_product_images") as mock_fetch:
                            with patch("image_checker.get_cached_image") as mock_get:
                                # Setup mocks
                                if scenario["cache"] is None:
                                    mock_get.side_effect = [None, scenario.get("cache_set", "null")]
                                else:
                                    mock_get.return_value = scenario["cache"]
                                
                                if "fetch" in scenario:
                                    mock_fetch.return_value = scenario["fetch"]
                                
                                if "ai" in scenario:
                                    mock_prepare.return_value = {"model": "test", "messages": []}
                                    mock_ai.return_value = scenario["ai"]
                                
                                mock_set.return_value = True
                                
                                # Execute
                                result = check_image_exists("12345")
                                
                                # Verify
                                assert result["imageExists"] == scenario["expected"]["imageExists"], \
                                    f"Scenario '{scenario['name']}' - imageExists mismatch"
                                assert result["IdProduto"] == scenario["expected"]["IdProduto"], \
                                    f"Scenario '{scenario['name']}' - IdProduto mismatch"
                                
                                # Verify cache set if applicable
                                if "cache_set" in scenario:
                                    if scenario["cache_set"] is None:
                                        mock_set.assert_called_with("12345", None)
                                    else:
                                        mock_set.assert_called_with("12345", scenario["cache_set"])


@pytest.mark.integration
class TestN8NCompatibilityEdgeCases:
    """Testes de casos extremos para garantir compatibilidade total."""

    def test_produto_id_with_special_chars(self):
        """Valida que produto_id com caracteres especiais funciona."""
        # N8N aceita qualquer string como produto_id
        special_ids = ["123-456", "produto_123", "123.456", "produto@123"]
        
        for produto_id in special_ids:
            with patch("image_checker.get_cached_image") as mock_get:
                mock_get.return_value = "base64_data"
                
                result = check_image_exists(produto_id)
                
                assert result["IdProduto"] == produto_id
                assert result["imageExists"] is True

    def test_empty_produto_id(self):
        """Valida que produto_id vazio funciona (edge case)."""
        # N8N aceita produto_id vazio
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = None
        
        result = check_image_exists("")
        
        assert result["IdProduto"] == ""
        # Comportamento pode variar, mas não deve quebrar

    def test_very_long_produto_id(self):
        """Valida que produto_id muito longo funciona."""
        # N8N aceita produto_id de qualquer tamanho
        long_id = "a" * 1000
        
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = "base64_data"
            
            result = check_image_exists(long_id)
            
            assert result["IdProduto"] == long_id

    def test_multiple_concurrent_requests_same_product(self):
        """Valida comportamento com múltiplas requisições simultâneas."""
        # Simula múltiplas requisições para o mesmo produto
        produto_id = "12345"
        
        with patch("image_checker.get_cached_image") as mock_get:
            mock_get.return_value = "base64_data"
            
            results = [check_image_exists(produto_id) for _ in range(5)]
            
            # Todas devem retornar o mesmo resultado
            for result in results:
                assert result["imageExists"] is True
                assert result["IdProduto"] == produto_id

