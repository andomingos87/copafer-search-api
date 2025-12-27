#!/usr/bin/env python3
"""
Script para identificar exatamente onde a paginação está falhando.
"""

import os
from dotenv import load_dotenv
from ingest_api import fetch_page

load_dotenv()

def test_pagination_boundaries():
    """Testa páginas específicas para encontrar onde a API para de retornar dados."""
    
    print("Testando limites de paginação...")
    print("=" * 60)
    
    # Primeira página para metadados
    first_page = fetch_page("*", 1, 50)
    total_pages = int(first_page.get("totalPages", 1))
    total_items = int(first_page.get("total", 0))
    
    print(f"API reporta: {total_pages} páginas, {total_items} itens totais")
    
    # Testa páginas próximas ao final
    test_ranges = [
        range(1, 6),           # Início
        range(1170, 1180),     # Onde parou (58528 ÷ 50 = ~1170)
        range(1530, 1536),     # Próximo ao final reportado
    ]
    
    for test_range in test_ranges:
        print(f"\nTestando páginas {test_range.start}-{test_range.stop-1}:")
        
        for page_num in test_range:
            if page_num > total_pages:
                print(f"  Página {page_num}: além do limite ({total_pages})")
                continue
                
            try:
                page_data = fetch_page("*", page_num, 50)
                items = page_data.get("items", [])
                items_count = len(items)
                
                # Verifica metadados da página
                reported_page = page_data.get("page")
                reported_total = page_data.get("total")
                reported_total_pages = page_data.get("totalPages")
                
                status = "✓" if items_count > 0 else "❌"
                print(f"  Página {page_num}: {status} {items_count} itens")
                
                if items_count == 0:
                    print(f"    Metadados: page={reported_page}, total={reported_total}, totalPages={reported_total_pages}")
                    
                    # Testa se é erro de API ou fim real
                    if reported_total_pages and page_num <= reported_total_pages:
                        print(f"    ⚠️  Página vazia mas deveria ter dados!")
                        
                        # Mostra estrutura da resposta
                        print(f"    Estrutura da resposta: {list(page_data.keys())}")
                        
                elif page_num > 1170 and page_num < 1180:
                    # Área crítica onde para - mostra primeiro item
                    if items:
                        first_item = items[0]
                        sku = first_item.get("codigo_produto", "N/A")
                        desc = first_item.get("descricao", "N/A")[:30]
                        print(f"    Primeiro item: SKU={sku}, Desc={desc}...")
                        
            except Exception as e:
                print(f"  Página {page_num}: ❌ ERRO - {e}")

def test_continuous_iteration():
    """Testa onde exatamente o iterador para."""
    
    print(f"\n" + "=" * 60)
    print("Testando onde o iterador para...")
    
    from ingest_api import iter_all_items
    
    count = 0
    last_page_items = 0
    current_page = 1
    
    try:
        for item in iter_all_items("*"):
            count += 1
            
            # A cada 50 itens (1 página), mostra progresso
            if count % 50 == 0:
                current_page = count // 50
                if count % 2500 == 0:  # A cada 50 páginas
                    print(f"  Página ~{current_page}: {count:,} itens coletados")
            
            # Para se chegou perto do limite conhecido
            if count >= 58600:
                break
                
    except Exception as e:
        print(f"Iterador falhou no item {count}: {e}")
    
    print(f"\nIterador parou em: {count:,} itens (~página {count//50})")

if __name__ == "__main__":
    test_pagination_boundaries()
    test_continuous_iteration()
