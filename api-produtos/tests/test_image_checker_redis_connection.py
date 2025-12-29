import redis
import os
from dotenv import load_dotenv

load_dotenv()

client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=os.getenv("REDIS_SSL", "false").lower() == "true",
    ssl_cert_reqs="none",  # Para Upstash
    decode_responses=True
)

try:
    client.ping()
    print("✅ Conexão OK!")
except Exception as e:
    print(f"❌ Erro: {e}")