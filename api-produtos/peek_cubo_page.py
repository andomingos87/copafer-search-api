import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Any

API_URL = "https://copafer.fortiddns.com/api/v2/cubo/produtos"
DEFAULT_TERMO = "*"
API_KEY = os.getenv(
    "X_COPAFER_KEY",
    "uwfWJVoMFBjBpBGvkzCYnq-zZyGREXxj-dG-XDWwpWdaaLOppmTtgTdptT",
)

def get(url: str) -> Any:
    headers = {
        "x-copafer-key": API_KEY,
        "Accept": "application/json",
        "User-Agent": "copafer-client/peek/1.0"
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        return json.loads(data.decode("utf-8"))


def main():
    # Tenta sem paginação explícita primeiro (page 1 default)
    params = {"termo": DEFAULT_TERMO}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    payload = get(url)

    print("Top-level keys:", list(payload.keys()))

    # tenta encontrar a lista de itens
    items = None
    for key in ("items", "data", "produtos", "results", "content"):
        if isinstance(payload.get(key), list):
            items = payload[key]
            print(f"Lista de itens encontrada em '{key}' com tamanho {len(items)}")
            break
    if items is None:
        # às vezes a lista vem aninhada
        for key, val in payload.items():
            if isinstance(val, dict):
                for k2 in ("items", "data", "produtos", "results", "content"):
                    if isinstance(val.get(k2), list):
                        items = val[k2]
                        print(f"Lista de itens encontrada em '{key}.{k2}' com tamanho {len(items)}")
                        break
            if items is not None:
                break

    if not items:
        print("Não encontrei lista de itens. Payload (resumo):")
        print(json.dumps(payload, ensure_ascii=False)[:2000])
        return 0

    print("Campos do primeiro item:")
    print(list(items[0].keys()))
    print("Primeiro item (resumo):")
    print(json.dumps(items[0], ensure_ascii=False)[:2000])

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
