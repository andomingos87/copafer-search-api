import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Tuple, Optional

API_URL = "https://copafer.fortiddns.com/api/v2/cubo/produtos"
DEFAULT_TERMO = "*"
# Permite sobrescrever a chave via variável de ambiente X_COPAFER_KEY; caso contrário usa a fornecida.
DEFAULT_API_KEY = os.getenv(
    "X_COPAFER_KEY",
    "uwfWJVoMFBjBpBGvkzCYnq-zZyGREXxj-dG-XDWwpWdaaLOppmTtgTdptT",
)


def fetch_totals(termo: str = DEFAULT_TERMO, timeout: int = 30) -> Tuple[Optional[int], Optional[int]]:
    """
    Chama a API do Cubo e retorna (total, totalPages).

    :param termo: termo de busca. Padrão: "*" (todos)
    :param timeout: timeout da requisição em segundos
    :return: tupla (total, totalPages). Se ocorrer erro ou campos não existirem, retorna (None, None)
    """
    params = {"termo": termo}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    headers = {
        "x-copafer-key": DEFAULT_API_KEY,
        "Accept": "application/json",
        "User-Agent": "copafer-client/1.0 (+https://example.local)"
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            # Tenta decodificar como JSON
            try:
                payload = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                # Conteúdo inesperado
                sys.stderr.write(f"Resposta não é JSON. Content-Type: {content_type}\n")
                return None, None

            # Extrai campos esperados
            total = payload.get("total")
            total_pages = payload.get("totalPages")
            return total, total_pages
    except urllib.error.HTTPError as e:
        # Erro HTTP da API
        body = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else ""
        sys.stderr.write(f"HTTPError {e.code}: {e.reason}. Corpo: {body}\n")
    except urllib.error.URLError as e:
        sys.stderr.write(f"URLError: {e.reason}\n")
    except Exception as e:
        sys.stderr.write(f"Erro inesperado: {e}\n")

    return None, None


def main(argv: list[str]) -> int:
    """
    Executa via CLI. Uso:
      python -m api.fetch_cubo_produtos [termo]
    ou
      python api/fetch_cubo_produtos.py [termo]
    """
    termo = argv[1] if len(argv) > 1 else DEFAULT_TERMO
    total, total_pages = fetch_totals(termo)

    result = {"total": total, "totalPages": total_pages}
    print(json.dumps(result, ensure_ascii=False))

    # Retorna código de status 0 se ambos presentes; senão 1
    if total is None or total_pages is None:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
