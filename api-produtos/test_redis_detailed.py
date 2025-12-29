#!/usr/bin/env python3
"""Teste detalhado de conexão Redis com múltiplas configurações."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import redis

# Carrega variáveis de ambiente
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=False)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

print("=" * 70)
print("TESTE DETALHADO DE CONEXÃO REDIS")
print("=" * 70)
print(f"Host: {REDIS_HOST}")
print(f"Port: {REDIS_PORT}")
print(f"Password: {'***' if REDIS_PASSWORD else '(não configurado)'}")
print("=" * 70)
print()

# Lista de configurações para testar
configs = [
    {
        "name": "Sem SSL, sem senha",
        "ssl": False,
        "password": None,
    },
    {
        "name": "Sem SSL, com senha",
        "ssl": False,
        "password": REDIS_PASSWORD if REDIS_PASSWORD else None,
    },
    {
        "name": "Com SSL, sem senha",
        "ssl": True,
        "password": None,
        "ssl_cert_reqs": "none",
    },
    {
        "name": "Com SSL, com senha",
        "ssl": True,
        "password": REDIS_PASSWORD if REDIS_PASSWORD else None,
        "ssl_cert_reqs": "none",
    },
    {
        "name": "Com SSL (required), com senha",
        "ssl": True,
        "password": REDIS_PASSWORD if REDIS_PASSWORD else None,
        "ssl_cert_reqs": "required",
    },
]

for i, config in enumerate(configs, 1):
    print(f"\n{'='*70}")
    print(f"Teste {i}/{len(configs)}: {config['name']}")
    print(f"{'='*70}")
    
    try:
        client_kwargs = {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": REDIS_DB,
            "decode_responses": True,
            "socket_connect_timeout": 5,
            "socket_timeout": 5,
        }
        
        if config.get("password"):
            client_kwargs["password"] = config["password"]
        
        if config.get("ssl"):
            client_kwargs["ssl"] = True
            client_kwargs["ssl_cert_reqs"] = config.get("ssl_cert_reqs", "none")
        
        print(f"Configuração: {client_kwargs}")
        print("Tentando conectar...")
        
        client = redis.Redis(**client_kwargs)
        result = client.ping()
        
        if result:
            print("✅ CONEXÃO BEM-SUCEDIDA!")
            print()
            
            # Testa operações
            print("Testando operações básicas...")
            test_key = "test_detailed"
            test_value = "test_123"
            
            client.set(test_key, test_value, ex=10)
            retrieved = client.get(test_key)
            client.delete(test_key)
            
            if retrieved == test_value:
                print("  ✅ SET/GET/DELETE: OK")
                print()
                print("🎉 CONFIGURAÇÃO FUNCIONANDO!")
                print()
                print("Use estas configurações no seu .env:")
                print(f"  REDIS_HOST={REDIS_HOST}")
                print(f"  REDIS_PORT={REDIS_PORT}")
                print(f"  REDIS_DB={REDIS_DB}")
                if config.get("password"):
                    print(f"  REDIS_PASSWORD={REDIS_PASSWORD}")
                else:
                    print("  # REDIS_PASSWORD não necessário")
                if config.get("ssl"):
                    print("  REDIS_SSL=true")
                    print(f"  # ssl_cert_reqs={config.get('ssl_cert_reqs', 'none')}")
                else:
                    print("  REDIS_SSL=false")
                sys.exit(0)
            else:
                print(f"  ⚠️  GET retornou valor diferente: {retrieved}")
        else:
            print("❌ PING retornou False")
            
    except redis.AuthenticationError as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO: {e}")
        print("   → Senha pode estar incorreta ou não é necessária")
        
    except redis.ConnectionError as e:
        error_str = str(e)
        if "10054" in error_str or "forçado" in error_str.lower():
            print(f"❌ CONEXÃO FECHADA PELO SERVIDOR: {e}")
            print("   → Servidor aceitou conexão mas fechou imediatamente")
            print("   → Possíveis causas:")
            print("     - Autenticação falhando (senha incorreta)")
            print("     - SSL/TLS necessário")
            print("     - Protocolo incompatível")
        elif "11001" in error_str or "getaddrinfo" in error_str.lower():
            print(f"❌ ERRO DNS: {e}")
            print("   → Hostname não pode ser resolvido")
        else:
            print(f"❌ ERRO DE CONEXÃO: {e}")
            
    except redis.TimeoutError as e:
        print(f"❌ TIMEOUT: {e}")
        
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {type(e).__name__}: {e}")

print()
print("=" * 70)
print("❌ NENHUMA CONFIGURAÇÃO FUNCIONOU")
print("=" * 70)
print()
print("🔍 DIAGNÓSTICO:")
print("   Todas as tentativas de conexão falharam.")
print()
print("💡 PRÓXIMOS PASSOS:")
print("   1. Verifique se o 'fly proxy' está rodando corretamente:")
print("      flyctl proxy 6379:6379")
print()
print("   2. Verifique se o proxy está apontando para o Redis correto:")
print("      flyctl status")
print()
print("   3. Verifique a senha no painel do Upstash/Fly.io")
print()
print("   4. Tente conectar diretamente (sem proxy) se o Redis for público")
print()
print("   5. Verifique os logs do fly proxy para mais detalhes")

