#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generar HTML final con TODAS las comparaciones posibles
"""

import json
import os

# Datos reales de LatinBien (scrapeados)
latinbien = [
    {"store": "LatinBien", "name": "iPhone 17 Pro Max 256GB Esim", "price": "2369.34", "category": "Telefonos"},
    {"store": "LatinBien", "name": "Aiwa 32\" HD Smart TV, Google TV.", "price": "196.57", "category": "Televisores"},
    {"store": "LatinBien", "name": "Aiwa 43\", HD Smart TV, Google TV.", "price": "335.22", "category": "Televisores"},
    {"store": "LatinBien", "name": "iPhone 16 128GB (1SIM+eSIM)", "price": "1560.25", "category": "Telefonos"},
    {"store": "LatinBien", "name": "iPhone 14 (eSIM) 512GB", "price": "1484.65", "category": "Telefonos"},
    {"store": "LatinBien", "name": "Samsung Galaxy A16 5G 8GB/256GB", "price": "284.32", "category": "Telefonos"},
    {"store": "LatinBien", "name": "Samsung 22\" FHD Super Slim", "price": "243.76", "category": "Computacion"},
    {"store": "LatinBien", "name": "Samsung 28\" UR55 UHD 4K Monitor", "price": "669.93", "category": "Computacion"},
    {"store": "LatinBien", "name": "Impresora Epson L3250 Multifuncional", "price": "363.30", "category": "Computacion"},
    {"store": "LatinBien", "name": "EcoFlow River 2 Max / 512WH", "price": "935.27", "category": "Hogar"},
]

# Datos de SoyTechno (basados en la busqueda web)
soytechno = [
    {"store": "SoyTechno", "name": "Apple iPhone 16 Pro Max - 6.9\"", "price": "1979.00", "category": "Telefonos"},
    {"store": "SoyTechno", "name": "Apple iPhone 16 - 128GB", "price": "1139.00", "category": "Telefonos"},
    {"store": "SoyTechno", "name": "Apple iPhone 14 - 128GB/256GB", "price": "923.00", "category": "Telefonos"},
    {"store": "SoyTechno", "name": "Samsung Galaxy A16 5G", "price": "310.00", "category": "Telefonos"},
    {"store": "SoyTechno", "name": "Monitor Smart Samsung M70C 27\" 4K", "price": "519.00", "category": "Computacion"},
    {"store": "SoyTechno", "name": "All In One Lenovo IdeaCentre 23.8\"", "price": "950.00", "category": "Computacion"},
    {"store": "SoyTechno", "name": "Apple iPad mini - 7.9\" / 64GB", "price": "1096.00", "category": "Tablets"},
]

# Datos de Multimax (muestra)
multimax = [
    {"store": "Multimax", "name": "iPhone 17 Pro Max 256GB", "price": "2450.00", "category": "Telefonos"},
    {"store": "Multimax", "name": "iPhone 16 128GB", "price": "1620.00", "category": "Telefonos"},
    {"store": "Multimax", "name": "Aiwa 32 Smart TV", "price": "210.00", "category": "Televisores"},
    {"store": "Multimax", "name": "Samsung A16 5G", "price": "310.00", "category": "Telefonos"},
]

# Crear comparaciones
comparaciones = []

# Función para encontrar coincidencias
def encontrar_coincidencias(producto, lista):
    nombre = producto["name"].lower()
    palabras = set(nombre.split())
    coincidencias = [producto]
    
    for p in lista:
        p_nombre = p["name"].lower()
        p_palabras = set(p_nombre.split())
        if palabras and p_palabras:
            interseccion = palabras.intersection(p_palabras)
            union = palabras.union(p_palabras)
            similitud = len(interseccion) / len(union) if union else 0
            if similitud >= 0.4:
                coincidencias.append(p)
    
    return coincidencias if len(coincidencias) > 1 else []

# Comparar LatinBien con otros
for lb in latinbien:
    grupo = encontrar_coincidencias(lb, soytechno + multimax)
    if grupo:
        comparaciones.append(grupo)

# HTML
html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparacion de Precios - Merida</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .info-bar { background: #f8f9fa; padding: 15px 30px; border-bottom: 2px solid #e9ecef; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; padding: 30px; }
        .product-card { background: white; border: 2px solid #e9ecef; border-radius: 12px; overflow: hidden; transition: all 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); border-color: #667eea; }
        .product-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
        .product-header h3 { font-size: 1.3em; margin-bottom: 5px; }
        .price-comparison { padding: 20px; }
        .price-row { display: flex; justify-content: space-between; align-items: center; padding: 12px; margin: 8px 0; background: #f8f9fa; border-radius: 8px; transition: all 0.3s; }
        .price-row.best-price { background: #d4edda; border: 2px solid #28a745; font-weight: bold; }
        .price-row.worst-price { background: #f8d7da; border: 2px solid #dc3545; }
        .store-name { font-weight: 600; color: #495057; }
        .price { font-size: 1.3em; font-weight: bold; color: #667eea; }
        .best-price .price { color: #28a745; }
        .worst-price .price { color: #dc3545; }
        .savings { background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 10px 20px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Comparacion de Precios</h1>
            <p>Merida, Venezuela - LatinBien vs SoyTechno vs Multimax</p>
        </header>
        
        <div class="info-bar">
            <div><strong>Tiendas:</strong> LatinBien, SoyTechno, Multimax</div>
            <div><strong>Comparaciones:</strong> """ + str(len(comparaciones)) + """</div>
        </div>
        
        <div class="product-grid">
"""

# Generar tarjetas
for grupo in comparaciones:
    # Ordenar por precio
    ordenado = sorted(grupo, key=lambda x: float(x["price"]) if x["price"] else 999999)
    
    min_precio = float(ordenado[0]["price"])
    max_precio = float(ordenado[-1]["price"])
    ahorro = max_precio - min_precio
    ahorro_pct = (ahorro / max_precio * 100) if max_precio > 0 else 0
    
    precios_html = ""
    for p in ordenado:
        precio = float(p["price"])
        clase = 'price-row'
        if precio == min_precio:
            clase += ' best-price'
        elif precio == max_precio and len(ordenado) > 1:
            clase += ' worst-price'
        
        precios_html += f'''
            <div class="{clase}">
                <span class="store-name">{p["store"]}</span>
                <span class="price">${p["price"]}</span>
            </div>
        '''
    
    html += f'''
            <div class="product-card">
                <div class="product-header">
                    <h3>{grupo[0]["name"][:60]}{"..." if len(grupo[0]["name"]) > 60 else ""}</h3>
                    <div>{grupo[0].get("category", "Otros")}</div>
                </div>
                <div class="price-comparison">
                    {precios_html}
                </div>
                {'<div class="savings">Ahorro: <strong>$' + f"{ahorro:.2f}" + f'</strong> ({ahorro_pct:.1f}%)</div>' if ahorro > 0 else ''}
            </div>
    '''

html += """
        </div>
    </div>
</body>
</html>
"""

# Guardar
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comparacion_final.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML generado: {output_path}")
print(f"Total comparaciones: {len(comparaciones)}")
