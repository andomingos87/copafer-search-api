#!/usr/bin/env python3
"""Script simples para testar conexão com Redis."""
import os
import sys
import socket
import logging
from pathlib import Path
from dotenv import load_dotenv
import redis

# Configura logging para ver mensagens
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=False)

# Lê configurações
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_SSL = os.getenv("REDIS_SSL", "false").lower() == "true"

print("=" * 60)
print("TESTE DE CONEXÃO REDIS")
print("=" * 60)
print(f"Host: {REDIS_HOST}")
print(f"Port: {REDIS_PORT}")
print(f"DB: {REDIS_DB}")
print(f"SSL: {REDIS_SSL}")
print(f"Password: {'***' if REDIS_PASSWORD else '(não configurado)'}")
print("=" * 60)
print()

# Detecta se é um endereço IPv6
def is_ipv6(host):
    return ':' in host and not host.startswith('[') and host.count(':') > 1

# Verifica se host contém porta (erro comum) - mas ignora IPv6
if ":" in REDIS_HOST and not is_ipv6(REDIS_HOST):
    print("⚠️  AVISO: REDIS_HOST contém ':' - pode estar incluindo a porta!")
    print(f"   Host atual: {REDIS_HOST}")
    print("   O host deve ser apenas o hostname, sem porta.")
    print()

# Testa resolução DNS primeiro (pula para IPv6 literal)
print("1. Testando resolução DNS...")
if is_ipv6(REDIS_HOST):
    print(f"   ℹ️  Host é um endereço IPv6 literal: {REDIS_HOST}")
    print(f"   ✅ Pulando resolução DNS para IPv6")
else:
    try:
        ip_address = socket.gethostbyname(REDIS_HOST)
        print(f"   ✅ DNS OK: {REDIS_HOST} -> {ip_address}")
    except socket.gaierror as e:
        print(f"   ❌ ERRO DNS: Não foi possível resolver {REDIS_HOST}")
        print(f"   Erro: {e}")
        print()
        print("🔍 DIAGNÓSTICO:")
        print("   O hostname não pode ser resolvido. Possíveis causas:")
        print("   1. Hostname incorreto no .env")
        print("   2. Problema de conexão com internet")
        print("   3. DNS não está funcionando")
        print("   4. Hostname não existe ou foi desativado")
        print()
        print("💡 SOLUÇÕES:")
        print("   1. Verifique o hostname no painel do Upstash/Fly.io")
        print("   2. Teste o hostname manualmente:")
        print(f"      nslookup {REDIS_HOST}")
        print("   3. Verifique se o Redis está configurado para acesso público")
        print("   4. Se for Redis privado na Fly.io, use 'fly proxy' para criar túnel")
        sys.exit(1)
    except Exception as e:
        print(f"   ⚠️  Erro ao testar DNS: {e}")
print()

# Testa conectividade TCP
print("2. Testando conectividade TCP...")
try:
    # Usa AF_INET6 para IPv6, AF_INET para IPv4
    addr_family = socket.AF_INET6 if is_ipv6(REDIS_HOST) else socket.AF_INET
    sock = socket.socket(addr_family, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((REDIS_HOST, REDIS_PORT))
    sock.close()
    if result == 0:
        print(f"   ✅ Porta {REDIS_PORT} está acessível")
    else:
        print(f"   ⚠️  Porta {REDIS_PORT} não está acessível (código: {result})")
        print("   Isso pode ser normal se SSL for necessário")
except Exception as e:
    print(f"   ⚠️  Erro ao testar porta: {e}")
print()

try:
    print("3. Tentando conectar ao Redis...")
    
    # Configura SSL para Upstash (ssl_cert_reqs="none")
    ssl_cert_reqs = "none" if REDIS_SSL else None
    
    print(f"   Configuração: SSL={REDIS_SSL}, ssl_cert_reqs={ssl_cert_reqs}")
    
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD if REDIS_PASSWORD else None,
        db=REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=10,
        ssl=REDIS_SSL,
        ssl_cert_reqs=ssl_cert_reqs,
    )
    
    # Testa conexão
    result = client.ping()
    
    if result:
        print("✅ CONEXÃO BEM-SUCEDIDA!")
        print()
        
        # Testa operações básicas
        print("Testando operações básicas...")
        
        # SET
        test_key = "test_connection"
        test_value = "test_value_123"
        client.set(test_key, test_value, ex=10)  # Expira em 10 segundos
        print("  ✅ SET: OK")
        
        # GET
        retrieved = client.get(test_key)
        if retrieved == test_value:
            print("  ✅ GET: OK")
        else:
            print(f"  ❌ GET: Esperado '{test_value}', recebido '{retrieved}'")
        
        # DELETE
        client.delete(test_key)
        print("  ✅ DELETE: OK")
        
        # INFO
        info = client.info("server")
        redis_version = info.get("redis_version", "desconhecida")
        print(f"  ✅ INFO: Redis versão {redis_version}")
        
        print()
        print("🎉 Todas as operações funcionaram corretamente!")
        
    else:
        print("❌ PING retornou False")
        sys.exit(1)
        
except redis.ConnectionError as e:
    print(f"❌ ERRO DE CONEXÃO: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    print()
    
    # Diagnóstico específico para erro 11001 (DNS)
    if "11001" in str(e) or "getaddrinfo failed" in str(e):
        print("🔍 DIAGNÓSTICO: Erro de resolução DNS (11001)")
        print()
        print("💡 SOLUÇÕES:")
        print("   1. Verifique se o hostname está correto no .env")
        print("   2. Teste resolução DNS manualmente:")
        print(f"      nslookup {REDIS_HOST}")
        print("   3. Se for Redis Upstash, verifique:")
        print("      - Hostname correto no painel")
        print("      - Se está configurado para acesso público")
        print("   4. Se for Redis na Fly.io:")
        print("      - Pode estar em rede privada")
        print("      - Use 'fly proxy 6379:6379' para criar túnel local")
        print("      - Ou configure para acesso público")
    else:
        print("Possíveis causas:")
        print("  1. Host ou porta incorretos")
        print("  2. Redis não está rodando")
        print("  3. Firewall bloqueando conexão")
        print("  4. SSL/TLS não configurado corretamente")
        print("  5. Senha incorreta")
    sys.exit(1)
    
except redis.AuthenticationError as e:
    print(f"❌ ERRO DE AUTENTICAÇÃO: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    print()
    print("Possíveis causas:")
    print("  1. Senha incorreta")
    print("  2. Usuário não tem permissão")
    sys.exit(1)
    
except redis.TimeoutError as e:
    print(f"❌ TIMEOUT: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    print()
    print("Possíveis causas:")
    print("  1. Rede lenta ou instável")
    print("  2. Redis não está respondendo")
    print("  3. Firewall bloqueando conexão")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ ERRO INESPERADO: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    import traceback
    print()
    print("Traceback completo:")
    traceback.print_exc()
    sys.exit(1)

