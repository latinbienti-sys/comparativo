#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Comparacion de Precios - Merida, Venezuela
Instrucciones de uso y ejemplos
"""

print("""
================================================================
     SISTEMA DE COMPARACION DE PRECIOS - MERIDA, VENEZUELA
================================================================

DESCRIPCION:
Este sistema permite comparar precios de productos electronicos
y electrodomesticos entre LatinBien y competidores locales.

ARCHIVOS CREADOS:
- latinbien_products.json    (productos extraidos de LatinBien)
- quick_comparison.json     (comparacion rapida con competidores)
- price_comparison_report.json (reporte completo)

COMO USAR:

1. EXTRAER DATOS DE LATINBIEN:
   python scraper_latinbien.py

2. COMPARAR CON COMPETIDORES (datos de muestra):
   python quick_test.py

3. VER RESULTADOS:
   - Revisar archivos .json generados
   - Los resultados muestran ahorros potenciales

COMPETIDORES INCLUIDOS (DATOS DE MUESTRA):
- Multimax (https://multimax.com.ve)
- MegaTecno (https://megatecno.com.ve)
- Frigilux (https://frigilux.com.ve)

CATEGORIAS MONITOREADAS:
- Telefonos (iPhones, Samsung, Xiaomi, etc.)
- Televisores (Smart TVs)
- Computacion (Laptops, Monitores)
- Hogar (Neveras, Lavadoras, Aires Acondicionados)

EJEMPLO DE SALIDA:
=============================================================
COMPARACION DE PRECIOS - MERIDA, VENEZUELA
=============================================================

## Producto 1: iPhone 17 Pro Max 256GB Esim...
------------------------------------------------------------
  LatinBien       | $   2369.34
  MegaTecno       | $   2420.00
  Multimax        | $   2450.00
  -> Ahorro: $80.66 (3.3%)

================================================================
""")

print("Para ejecutar el sistema completo:")
print("1. python scraper_latinbien.py")
print("2. python quick_test.py")
print("\nO directamente: python quick_test.py (si ya tienes datos)")
