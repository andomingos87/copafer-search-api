#!/usr/bin/env python3
"""
Script para debugar a paginação e verificar se todas as páginas estão sendo processadas.
"""

import os
from dotenv import load_dotenv
from ingest_api import fetch_page, iter_all_items

load_dotenv()

def debug_pagination():
    """Verifica se a paginação está funcionando corretamente."""
    
    print("Debugando paginação da API do Cubo...")
    print("=" * 60)
    
    # Primeira página para pegar metadados
    try:
        first_page = fetch_page("*", 1, 50)
        total_pages = int(first_page.get("totalPages", 1))
        total_items = int(first_page.get("total", 0))
        current_page = int(first_page.get("page", 1))
        limit = int(first_page.get("limit", 50))
        
        print(f"Metadados da primeira página:")
        print(f"  Total de páginas: {total_pages}")
        print(f"  Total de itens: {total_items}")
        print(f"  Página atual: {current_page}")
        print(f"  Limite por página: {limit}")
        print(f"  Itens na primeira página: {len(first_page.get('items', []))}")
        
        # Testa algumas páginas específicas
        test_pages = [1, 100, 500, 1000, total_pages-1, total_pages]
        
        print(f"\nTestando páginas específicas:")
        for page_num in test_pages:
            if page_num <= 0 or page_num > total_pages:
                continue
                
            try:
                page_data = fetch_page("*", page_num, 50)
                items_count = len(page_data.get("items", []))
                page_reported = page_data.get("page", "?")
                
                print(f"  Página {page_num}: {items_count} itens (API reporta página {page_reported})")
                
                if items_count == 0:
                    print(f"    ⚠️  Página {page_num} está vazia!")
                    
            except Exception as e:
                print(f"    ❌ Erro na página {page_num}: {e}")
        
        # Testa o iterador completo em uma amostra
        print(f"\nTestando iterador completo (primeiras 5 páginas):")
        count = 0
        pages_seen = set()
        
        for item in iter_all_items("*", limit_pages=5):
            count += 1
            # Tenta extrair informação de página se disponível
            
        print(f"  Itens coletados pelo iterador: {count}")
        print(f"  Esperado (5 páginas × 50): 250")
        
        if count != 250:
            print(f"    ⚠️  Discrepância detectada!")
            
    except Exception as e:
        print(f"Erro durante debug: {e}")

def test_full_iteration_count():
    """Conta todos os itens usando o iterador (sem limite de páginas)."""
    print(f"\n" + "=" * 60)
    print("Testando contagem completa com iterador...")
    
    try:
        count = 0
        for item in iter_all_items("*"):
            count += 1
            if count % 5000 == 0:
                print(f"  Processados: {count:,}")
        
        print(f"\nTotal de itens coletados pelo iterador: {count:,}")
        print(f"Total esperado da API: 76.720")
        
        if count != 76720:
            diff = 76720 - count
            print(f"Diferença: {diff:,} itens ({(diff/76720)*100:.1f}%)")
            
    except Exception as e:
        print(f"Erro durante contagem completa: {e}")

if __name__ == "__main__":
    debug_pagination()
    
    # Pergunta se quer fazer teste completo
    response = input("\nFazer teste de contagem completa? (pode demorar) [y/N]: ")
    if response.lower() in ['y', 'yes', 's', 'sim']:
        test_full_iteration_count()
