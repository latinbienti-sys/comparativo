#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Comparacion de Precios - Merida, Venezuela
Compara precios entre LatinBien y competidores locales
"""

import sys
import os

def main():
    print("""
==============================================================
     SISTEMA DE COMPARACION DE PRECIOS - MERIDA, VENEZUELA
==============================================================
    """)
    
    print("1. Ejecutar scrapers (recolectar datos)")
    print("2. Comparar precios")
    print("3. Ejecutar todo (scrape + compare)")
    print("4. Salir")
    
    choice = input("\nSeleccione una opción: ")
    
    if choice == '1':
        run_scrapers()
    elif choice == '2':
        run_comparison()
    elif choice == '3':
        run_scrapers()
        run_comparison()
    elif choice == '4':
        sys.exit(0)
    else:
        print("Opción inválida")

def run_scrapers():
    """Run all scrapers"""
    print("\n--- Ejecutando Scrapers ---\n")
    
    # LatinBien
    try:
        from scraper_latinbien import LatinBienScraper
        print("Scraping LatinBien...")
        lb = LatinBienScraper()
        lb.scrape_products(max_pages=2)
        lb.save_to_json()
    except Exception as e:
        print(f"Error scraping LatinBien: {e}")
    
    # Multimax
    try:
        from scraper_multimax import MultimaxScraper
        print("\nScraping Multimax...")
        mm = MultimaxScraper()
        mm.scrape_products()
        mm.save_to_json()
    except Exception as e:
        print(f"Error scraping Multimax: {e}")
    
    print("\n✓ Scraping completado!")

def run_comparison():
    """Run price comparison"""
    print("\n--- Comparando Precios ---\n")
    
    try:
        from comparator import PriceComparator
        
        comparator = PriceComparator()
        
        # Check if data files exist
        data_files = []
        for f in ['latinbien_products.json', 'multimax_products.json']:
            if os.path.exists(f):
                data_files.append(f)
        
        if not data_files:
            print("No se encontraron archivos de datos. Ejecute primero los scrapers.")
            return
        
        comparator.load_products(*data_files)
        
        # Generate report
        report = comparator.generate_report()
        
        # Print summary
        print("\n" + "="*60)
        print("RESUMEN")
        print("="*60)
        print(f"Total productos: {report['summary']['total_products']}")
        print(f"Tiendas: {', '.join(report['summary']['stores'])}")
        print(f"Categorías: {', '.join(report['summary']['categories'])}")
        
        # Print best deals
        print("\n" + "="*60)
        print("MEJORES OFERTAS (productos con diferencia de precio)")
        print("="*60)
        
        for category, comparisons in report['comparisons'].items():
            if comparisons:
                print(f"\n## {category}")
                for comp in comparisons[:5]:  # Show top 5 per category
                    best = min(comp['products'], key=lambda x: float(x['price']) if x['price'] else 999999)
                    print(f"  {best['store']}: {best['name'][:50]}... ${best['price']}")
        
        print("\n✓ Comparación completada!")
        print("Reporte guardado en: price_comparison_report.json")
        
    except Exception as e:
        print(f"Error en comparación: {e}")

if __name__ == "__main__":
    main()
