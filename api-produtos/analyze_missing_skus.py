#!/usr/bin/env python3
"""
Script para analisar quantos produtos da API do Cubo não têm SKU válido.
Ajuda a entender por que 19.141 produtos estão sendo perdidos na ingestão.
"""

import os
import sys
from dotenv import load_dotenv
from ingest_api import iter_all_items, map_item_to_row, norm_str

load_dotenv()

def analyze_sku_issues(limit_pages=5):
    """Analisa produtos sem SKU válido nas primeiras páginas."""
    
    print(f"Analisando primeiras {limit_pages} páginas da API do Cubo...")
    print("=" * 60)
    
    total_items = 0
    valid_skus = 0
    invalid_skus = 0
    empty_skus = 0
    only_dots_skus = 0
    
    # Amostras de SKUs problemáticos
    empty_samples = []
    dots_samples = []
    
    try:
        for item in iter_all_items("*", limit_pages=limit_pages):
            total_items += 1
            
            # Pega o SKU cru
            raw_sku = item.get("codigo_produto")
            normalized_sku = norm_str(raw_sku)
            
            if not normalized_sku:
                empty_skus += 1
                if len(empty_samples) < 5:
                    empty_samples.append({
                        "raw": raw_sku,
                        "descricao": item.get("descricao", "")[:50]
                    })
            else:
                # Aplica a mesma lógica do map_item_to_row
                processed_sku = normalized_sku.replace(".", "").strip()
                if not processed_sku:
                    only_dots_skus += 1
                    if len(dots_samples) < 5:
                        dots_samples.append({
                            "raw": raw_sku,
                            "normalized": normalized_sku,
                            "descricao": item.get("descricao", "")[:50]
                        })
                else:
                    valid_skus += 1
            
            # Testa se map_item_to_row retorna None
            row = map_item_to_row(item)
            if not row:
                invalid_skus += 1
    
    except Exception as e:
        print(f"Erro durante análise: {e}")
        return
    
    # Relatório
    print(f"Total de itens analisados: {total_items}")
    print(f"SKUs válidos: {valid_skus}")
    print(f"SKUs inválidos (rejeitados): {invalid_skus}")
    print(f"  - SKUs vazios/None: {empty_skus}")
    print(f"  - SKUs só com pontos: {only_dots_skus}")
    print()
    
    if total_items > 0:
        rejection_rate = (invalid_skus / total_items) * 100
        print(f"Taxa de rejeição: {rejection_rate:.1f}%")
        
        # Extrapolação para o total
        if rejection_rate > 0:
            estimated_lost = int(76720 * (rejection_rate / 100))
            print(f"Estimativa de produtos perdidos no total: ~{estimated_lost:,}")
    
    print("\n" + "=" * 60)
    
    # Amostras de problemas
    if empty_samples:
        print("Amostras de produtos com SKU vazio:")
        for i, sample in enumerate(empty_samples, 1):
            print(f"  {i}. Raw: {repr(sample['raw'])} | Desc: {sample['descricao']}")
    
    if dots_samples:
        print("\nAmostras de produtos com SKU só pontos:")
        for i, sample in enumerate(dots_samples, 1):
            print(f"  {i}. Raw: {repr(sample['raw'])} -> {repr(sample['normalized'])} | Desc: {sample['descricao']}")

if __name__ == "__main__":
    # Permite passar número de páginas como argumento
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    analyze_sku_issues(pages)
