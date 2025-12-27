import os
import sys
import time
import math
import argparse
import json
from typing import Any, Dict, Iterable, List, Optional, Tuple
from datetime import datetime

import requests
from dotenv import load_dotenv
from tqdm import tqdm

# Reuso de funções seguras do ingest_csv.py
from ingest_csv import (
    connect_db,
    norm_str,
    parse_decimal_br,
    chunk_by_tokens,
    build_product_text,
    upsert_product,
    insert_chunks,
)

load_dotenv()

API_URL = os.getenv("CUBO_API_URL", "https://copafer.fortiddns.com/api/v2/cubo/produtos")
API_KEY = os.getenv("X_COPAFER_KEY", "")

# Defaults seguros
DEFAULT_LIMIT = int(os.getenv("CUBO_PAGE_LIMIT", "50"))  # confirmado: 50
DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = "copafer-client/ingest_api/1.0"


def _headers() -> Dict[str, str]:
    if not API_KEY:
        raise RuntimeError("Defina X_COPAFER_KEY no .env")
    return {
        "x-copafer-key": API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": DEFAULT_USER_AGENT,
    }


def fetch_page(termo: str, page: int, limit: int = DEFAULT_LIMIT, timeout: int = DEFAULT_TIMEOUT, verbose: bool = False) -> Dict[str, Any]:
    params = {"termo": termo, "page": page, "limit": limit}
    if verbose:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Buscando página {page} (limit={limit})...")
    
    resp = requests.get(API_URL, headers=_headers(), params=params, timeout=timeout)
    # retries para 5xx
    if resp.status_code >= 500:
        if verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] API retornou {resp.status_code}, iniciando retry...")
        # simples backoff
        for i in range(3):
            sleep_time = 1.5 * (2 ** i)
            if verbose:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Tentativa {i+1}/3, aguardando {sleep_time:.1f}s...")
            time.sleep(sleep_time)
            resp = requests.get(API_URL, headers=_headers(), params=params, timeout=timeout)
            if resp.ok:
                if verbose:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Retry bem-sucedido!")
                break
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError as e:
        raise RuntimeError(f"Resposta não é JSON: {e}\nCorpo: {resp.text[:500]}")


def iter_all_items(termo: str, start_page: int = 1, limit_pages: Optional[int] = None, page_size: int = DEFAULT_LIMIT, verbose: bool = False) -> Iterable[Dict[str, Any]]:
    """
    Itera por todas as páginas, emitindo itens um a um.
    Usa os campos totalPages/total se disponíveis para delimitar o range.
    """
    page = start_page
    pages_processed = 0

    # primeira chamada para descobrir totalPages
    payload = fetch_page(termo, page, page_size, verbose=verbose)
    total_pages = int(payload.get("totalPages") or 1)
    total_items = int(payload.get("total") or 0)
    
    if verbose:
        pages_to_process = min(limit_pages or total_pages, total_pages - start_page + 1)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando ingestão:")
        print(f"  Total de páginas na API: {total_pages}")
        print(f"  Total de itens na API: {total_items:,}")
        print(f"  Páginas a processar: {pages_to_process}")
        print(f"  Página inicial: {start_page}")
        print(f"  Itens por página: {page_size}")

    def extract_items(p: Dict[str, Any]) -> List[Dict[str, Any]]:
        # API do Cubo usa 'produtos'; fallback para outros campos conhecidos
        items = None
        if isinstance(p.get("produtos"), list):
            items = p["produtos"]
        elif isinstance(p.get("items"), list):
            items = p["items"]
        else:
            for key in ("data", "results", "content"):
                val = p.get(key)
                if isinstance(val, list):
                    items = val
                    break
                if isinstance(val, dict) and isinstance(val.get("items"), list):
                    items = val["items"]
                    break
        return items or []

    while True:
        cur_payload = payload if page == start_page else fetch_page(termo, page, page_size, verbose=verbose)
        items = extract_items(cur_payload)
        
        if verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Página {page}/{total_pages}: {len(items)} itens")
        
        for it in items:
            yield it

        pages_processed += 1
        if limit_pages is not None and pages_processed >= limit_pages:
            if verbose:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Limite de páginas atingido ({limit_pages})")
            break
        page += 1
        if page > total_pages:
            if verbose:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Todas as páginas processadas")
            break


def filter_raw_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Remove campos de preço do raw e normaliza valores simples para string.
    Regras:
    - Remove chaves cujo nome contenha 'preco' ou 'price'.
    - Mantém demais campos convertendo para string simples quando aplicável.
    """
    out: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        kl = str(k).lower()
        if "preco" in kl or "price" in kl:
            continue
        try:
            # JSON serializável; mantém valor como está
            json.dumps(v)
            out[k] = v
        except Exception:
            out[k] = str(v)
    return out


def map_item_to_row(it: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Mapeia um item do payload para o dicionário de colunas esperadas no DB.
    Campos esperados, seguindo ingest_csv.py:
      sku -> codigo_produto (removendo pontos)
      name -> descricao
      description -> descricao_tecnica
      codigo_barras -> codigo_barras
      tipo -> tipo
      um -> um
      qtde_cx -> qtde_cx
      estoque -> estoque (convertendo BR -> Decimal via parse_decimal_br)
    """
    sku = norm_str(it.get("codigo_produto"))
    if sku:
        sku = sku.replace(".", "").strip()
    if not sku:
        return None

    name = norm_str(it.get("descricao"))
    desc = norm_str(it.get("descricao_tecnica"))
    codigo_barras = norm_str(it.get("codigo_barras"))
    tipo = norm_str(it.get("tipo"))
    um = norm_str(it.get("um"))
    qtde_cx = norm_str(it.get("qtde_cx"))
    estoque = parse_decimal_br(it.get("estoque"))

    raw_filtered = filter_raw_payload(it)

    return {
        "sku": sku,
        "name": name,
        "description": desc,
        "codigo_barras": codigo_barras,
        "tipo": tipo,
        "um": um,
        "qtde_cx": qtde_cx,
        "estoque": estoque,
        "raw": json.dumps(raw_filtered, ensure_ascii=False),
    }


def ingest_from_api(
    *,
    termo: str = "*",
    page_size: int = DEFAULT_LIMIT,
    start_page: int = 1,
    limit_pages: Optional[int] = None,
    dry_run: bool = False,
    commit_every: int = 200,
    verbose: bool = False,
) -> Tuple[int, int]:
    """
    Faz a ingestão iterando sobre a API paginada.
    Retorna (upserts_em_products, total_chunks_inseridos)
    """
    upserted = 0
    chunks_ins = 0
    start_time = datetime.now()
    
    if verbose:
        print(f"[{start_time.strftime('%H:%M:%S')}] Iniciando ingestão {'(DRY RUN)' if dry_run else '(PRODUÇÃO)'}")
        print(f"  Termo: '{termo}'")
        print(f"  Commit a cada: {commit_every} produtos")

    with connect_db() as con:
        con.autocommit = False
        with con.cursor() as cur:
            batch_count = 0
            
            # Configura barra de progresso se verbose
            iterator = iter_all_items(termo, start_page=start_page, limit_pages=limit_pages, page_size=page_size, verbose=verbose)
            
            if verbose:
                # Estima total de itens para barra de progresso
                estimated_items = (limit_pages or 1535) * page_size
                iterator = tqdm(iterator, total=estimated_items, desc="Processando produtos", unit="item")
            
            for it in iterator:
                row = map_item_to_row(it)
                if not row:
                    continue

                if dry_run:
                    upserted += 1
                    # só valida chunking sem gravar
                    text = build_product_text({
                        "descricao": row["name"],
                        "tipo": row["tipo"],
                        "descricao_tecnica": row["description"],
                        "codigo_produto": row["sku"],
                        "codigo_barras": row["codigo_barras"],
                    })
                    _ = chunk_by_tokens(text)
                else:
                    product_id = upsert_product(cur, row)
                    upserted += 1

                    text = build_product_text({
                        "descricao": row["name"],
                        "tipo": row["tipo"],
                        "descricao_tecnica": row["description"],
                        "codigo_produto": row["sku"],
                        "codigo_barras": row["codigo_barras"],
                    })
                    chunks = chunk_by_tokens(text)
                    
                    if verbose and upserted % 64 == 0:  # Log a cada lote de embeddings
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Gerando embeddings para lote {(upserted-1)//64 + 1} ({len(chunks)} chunks)...")
                    
                    insert_chunks(cur, product_id, chunks)
                    chunks_ins += len(chunks)

                    batch_count += 1
                    if batch_count % commit_every == 0:
                        if verbose:
                            elapsed = datetime.now() - start_time
                            rate = upserted / elapsed.total_seconds() * 60  # produtos/min
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] Commit #{batch_count//commit_every}: {upserted:,} produtos, {chunks_ins:,} chunks ({rate:.1f} prod/min)")
                        con.commit()

            if not dry_run:
                # otimiza planos ao final
                if verbose:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Otimizando índices do banco...")
                cur.execute("ANALYZE rag.products;")
                cur.execute("ANALYZE rag.product_chunks;")
        if not dry_run:
            con.commit()
    
    end_time = datetime.now()
    elapsed = end_time - start_time
    
    if verbose:
        print(f"[{end_time.strftime('%H:%M:%S')}] Ingestão concluída!")
        print(f"  Tempo total: {elapsed}")
        print(f"  Produtos processados: {upserted:,}")
        if not dry_run:
            print(f"  Chunks inseridos: {chunks_ins:,}")
            if elapsed.total_seconds() > 0:
                rate = upserted / elapsed.total_seconds() * 60
                print(f"  Taxa média: {rate:.1f} produtos/min")

    return upserted, chunks_ins


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--termo", default="*", help="termo de busca na API do Cubo")
    ap.add_argument("--page-size", type=int, default=DEFAULT_LIMIT, help="tamanho da página (padrão 50)")
    ap.add_argument("--start-page", type=int, default=1, help="página inicial (1-based)")
    ap.add_argument("--limit-pages", type=int, default=None, help="limite de páginas a processar (útil para testes)")
    ap.add_argument("--dry-run", action="store_true", help="não grava no banco, apenas valida fluxo")
    ap.add_argument("--verbose", "-v", action="store_true", help="exibe logs detalhados de progresso")

    args = ap.parse_args(argv[1:])

    upserted, chunks_ins = ingest_from_api(
        termo=args.termo,
        page_size=args.page_size,
        start_page=args.start_page,
        limit_pages=args.limit_pages,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    print(json.dumps({
        "ok": True,
        "dry_run": args.dry_run,
        "upserted_products": upserted,
        "inserted_chunks": chunks_ins,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
