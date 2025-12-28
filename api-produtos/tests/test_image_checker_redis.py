"""Testes unitários para funções Redis do image_checker."""
import pytest
from unittest.mock import Mock, MagicMock, patch
import redis
from image_checker import (
    get_redis_client,
    get_cached_image,
    set_cached_image,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
    REDIS_SSL,
    IMAGE_CACHE_TTL,
)


@pytest.mark.unit
class TestGetRedisClient:
    """Testes para get_redis_client."""

    @patch("image_checker.redis.Redis")
    def test_returns_client_when_ping_succeeds(self, mock_redis_class):
        """Retorna cliente quando ping() funciona."""
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_redis_class.return_value = mock_client

        result = get_redis_client()

        assert result is not None
        assert result == mock_client
        mock_redis_class.assert_called_once_with(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD if REDIS_PASSWORD else None,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            ssl=REDIS_SSL,
            ssl_cert_reqs="required" if REDIS_SSL else None,
        )
        mock_client.ping.assert_called_once()

    @patch("image_checker.redis.Redis")
    def test_returns_none_when_ping_fails(self, mock_redis_class):
        """Retorna None quando ping() falha."""
        mock_client = MagicMock()
        mock_client.ping.side_effect = redis.ConnectionError("Connection failed")
        mock_redis_class.return_value = mock_client

        result = get_redis_client()

        assert result is None

    @patch("image_checker.redis.Redis")
    def test_returns_none_when_connection_fails(self, mock_redis_class):
        """Retorna None quando conexão falha."""
        mock_redis_class.side_effect = redis.ConnectionError("Connection failed")

        result = get_redis_client()

        assert result is None


@pytest.mark.unit
class TestGetCachedImage:
    """Testes para get_cached_image."""

    @patch("image_checker.get_redis_client")
    def test_returns_value_when_exists(self, mock_get_client):
        """Retorna valor quando existe no cache."""
        mock_client = MagicMock()
        mock_client.get.return_value = "base64_image_data"
        mock_get_client.return_value = mock_client

        result = get_cached_image("12345")

        assert result == "base64_image_data"
        mock_client.get.assert_called_once_with("best_image_for_12345")

    @patch("image_checker.get_redis_client")
    def test_returns_null_string_when_cached_as_null(self, mock_get_client):
        """Retorna string 'null' quando produto foi marcado como sem imagem."""
        mock_client = MagicMock()
        mock_client.get.return_value = "null"
        mock_get_client.return_value = mock_client

        result = get_cached_image("12345")

        assert result == "null"

    @patch("image_checker.get_redis_client")
    def test_returns_none_when_key_not_found(self, mock_get_client):
        """Retorna None quando chave não existe."""
        mock_client = MagicMock()
        mock_client.get.return_value = None
        mock_get_client.return_value = mock_client

        result = get_cached_image("12345")

        assert result is None

    @patch("image_checker.get_redis_client")
    def test_returns_none_when_redis_unavailable(self, mock_get_client):
        """Retorna None quando Redis indisponível."""
        mock_get_client.return_value = None

        result = get_cached_image("12345")

        assert result is None

    @patch("image_checker.get_redis_client")
    def test_returns_none_on_redis_error(self, mock_get_client):
        """Retorna None quando ocorre erro no Redis."""
        mock_client = MagicMock()
        mock_client.get.side_effect = redis.RedisError("Redis error")
        mock_get_client.return_value = mock_client

        result = get_cached_image("12345")

        assert result is None


@pytest.mark.unit
class TestSetCachedImage:
    """Testes para set_cached_image."""

    @patch("image_checker.get_redis_client")
    def test_saves_base64_with_ttl(self, mock_get_client):
        """Grava base64 com TTL padrão."""
        mock_client = MagicMock()
        mock_client.setex.return_value = True
        mock_get_client.return_value = mock_client

        result = set_cached_image("12345", "base64_image_data")

        assert result is True
        mock_client.setex.assert_called_once_with(
            "best_image_for_12345",
            IMAGE_CACHE_TTL,
            "base64_image_data"
        )

    @patch("image_checker.get_redis_client")
    def test_saves_base64_with_custom_ttl(self, mock_get_client):
        """Grava base64 com TTL customizado."""
        mock_client = MagicMock()
        mock_client.setex.return_value = True
        mock_get_client.return_value = mock_client

        result = set_cached_image("12345", "base64_image_data", ttl=3600)

        assert result is True
        mock_client.setex.assert_called_once_with(
            "best_image_for_12345",
            3600,
            "base64_image_data"
        )

    @patch("image_checker.get_redis_client")
    def test_saves_null_string_when_base64_is_none(self, mock_get_client):
        """Grava string 'null' quando base64_value é None."""
        mock_client = MagicMock()
        mock_client.setex.return_value = True
        mock_get_client.return_value = mock_client

        result = set_cached_image("12345", None)

        assert result is True
        mock_client.setex.assert_called_once_with(
            "best_image_for_12345",
            IMAGE_CACHE_TTL,
            "null"
        )

    @patch("image_checker.get_redis_client")
    def test_returns_false_when_redis_unavailable(self, mock_get_client):
        """Retorna False quando Redis indisponível."""
        mock_get_client.return_value = None

        result = set_cached_image("12345", "base64_image_data")

        assert result is False

    @patch("image_checker.get_redis_client")
    def test_returns_false_on_redis_error(self, mock_get_client):
        """Retorna False quando ocorre erro no Redis."""
        mock_client = MagicMock()
        mock_client.setex.side_effect = redis.RedisError("Redis error")
        mock_get_client.return_value = mock_client

        result = set_cached_image("12345", "base64_image_data")

        assert result is False

