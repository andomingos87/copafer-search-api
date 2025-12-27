#!/usr/bin/env python3
"""
Script para analisar a estrutura exata da resposta da API do Cubo.
"""

import os
import json
from dotenv import load_dotenv
from ingest_api import fetch_page

load_dotenv()

def analyze_response_structure():
    """Analisa a estrutura da resposta da API."""
    
    print("Analisando estrutura da resposta da API do Cubo...")
    print("=" * 60)
    
    try:
        # Testa primeira página
        response = fetch_page("*", 1, 50)
        
        print("Estrutura completa da resposta:")
        print(json.dumps(response, indent=2, ensure_ascii=False)[:2000] + "...")
        
        print(f"\nChaves na resposta: {list(response.keys())}")
        
        # Analisa cada campo
        for key, value in response.items():
            print(f"\n{key}: {type(value)}")
            if isinstance(value, list):
                print(f"  Lista com {len(value)} itens")
                if value and isinstance(value[0], dict):
                    print(f"  Primeiro item tem chaves: {list(value[0].keys())[:10]}...")
            elif isinstance(value, dict):
                print(f"  Dict com chaves: {list(value.keys())}")
            else:
                print(f"  Valor: {value}")
        
        # Testa extract_items atual
        from ingest_api import iter_all_items
        
        print(f"\n" + "=" * 60)
        print("Testando extract_items com a função corrigida:")
        
        count = 0
        for item in iter_all_items("*", limit_pages=1):
            count += 1
            if count == 1:
                print(f"Primeiro item extraído: {list(item.keys())[:10]}...")
            if count >= 50:
                break
        
        print(f"Itens extraídos da primeira página: {count}")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_response_structure()
