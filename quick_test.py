#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to compare LatinBien prices with manual competitor data
"""
import json
import re

# Sample competitor prices (Merida, Venezuela)
competitors = {
    "Multimax": [
        {"name": "iPhone 17 Pro Max 256GB", "price": "2450.00", "category": "Telefonos"},
        {"name": "iPhone 16 128GB", "price": "1620.00", "category": "Telefonos"},
        {"name": "Aiwa 32 Smart TV", "price": "210.00", "category": "Televisores"},
        {"name": "Samsung A16 5G", "price": "310.00", "category": "Telefonos"},
    ],
    "Frigilux": [
        {"name": "Lavadora Automatica 24Kg", "price": "820.00", "category": "Hogar"},
        {"name": "Aire Acondicionado 18K BTU", "price": "890.00", "category": "Hogar"},
    ],
    "MegaTecno": [
        {"name": "iPhone 17 Pro Max 256GB", "price": "2420.00", "category": "Telefonos"},
        {"name": "Laptop Gaming", "price": "1200.00", "category": "Computacion"},
    ]
}

def normalize_name(name):
    """Normalize product name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def find_matches(latinbien_products, threshold=0.6):
    """Find matching products across stores"""
    matches = []
    
    for lb_product in latinbien_products:
        lb_norm = normalize_name(lb_product['name'])
        lb_words = set(lb_norm.split())
        
        matching_products = [lb_product]
        
        for store, products in competitors.items():
            for comp_product in products:
                comp_norm = normalize_name(comp_product['name'])
                comp_words = set(comp_norm.split())
                
                if lb_words and comp_words:
                    intersection = lb_words.intersection(comp_words)
                    union = lb_words.union(comp_words)
                    similarity = len(intersection) / len(union)
                    
                    if similarity >= threshold:
                        matching_products.append({
                            'store': store,
                            'name': comp_product['name'],
                            'price': comp_product['price'],
                            'category': comp_product['category']
                        })
        
        if len(matching_products) > 1:
            matches.append(matching_products)
    
    return matches

def print_comparison(matches):
    """Print price comparison"""
    print("\n" + "="*70)
    print("COMPARACION DE PRECIOS - MERIDA, VENEZUELA")
    print("="*70)
    
    for i, match_group in enumerate(matches, 1):
        print(f"\n## Producto {i}: {match_group[0]['name'][:50]}...")
        print("-" * 60)
        
        # Sort by price
        sorted_group = sorted(match_group, key=lambda x: float(x['price']))
        
        for product in sorted_group:
            print(f"  {product['store']:15} | ${product['price']:>10}")
        
        # Calculate savings
        prices = [float(p['price']) for p in sorted_group]
        if len(prices) > 1:
            min_price = min(prices)
            max_price = max(prices)
            savings = max_price - min_price
            savings_pct = (savings / max_price * 100)
            print(f"  -> Ahorro: ${savings:.2f} ({savings_pct:.1f}%)")

if __name__ == "__main__":
    # Load LatinBien products
    with open('latinbien_products.json', 'r', encoding='utf-8') as f:
        latinbien = json.load(f)
    
    print(f"LatinBien products loaded: {len(latinbien)}")
    print(f"Competitor samples: {sum(len(v) for v in competitors.values())}")
    
    # Find matches
    matches = find_matches(latinbien)
    
    # Print comparison
    print_comparison(matches)
    
    # Save results
    results = {
        'latinbien_count': len(latinbien),
        'matches': matches
    }
    
    with open('quick_comparison.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResultados guardados en: quick_comparison.json")
