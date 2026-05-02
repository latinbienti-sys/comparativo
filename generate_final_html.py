#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generar HTML final con todos los datos
"""

import json
import os

# Cargar datos existentes
try:
    with open('quick_comparison.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    data = {"matches": [], "latinbien_count": 0}

# Añadir más productos de SoyTechno basados en datos reales
nuevos_productos = [
    # Telefonos
    {"store": "SoyTechno", "name": "Apple iPhone 17 Pro Max 256GB", "price": "1979.00", "category": "Telefonos"},
    {"store": "LatinBien", "name": "iPhone 17 Pro Max 256GB Esim", "price": "2369.34", "category": "Telefonos"},
    
    {"store": "SoyTechno", "name": "Apple iPhone 16 128GB", "price": "1139.00", "category": "Telefonos"},
    {"store": "LatinBien", "name": "iPhone 16 128GB (1SIM+eSIM)", "price": "1560.25", "category": "Telefonos"},
    
    {"store": "SoyTechno", "name": "Samsung Galaxy A16 5G", "price": "310.00", "category": "Telefonos"},
    {"store": "LatinBien", "name": "Samsung Galaxy A16 5G 8GB/256GB", "price": "284.32", "category": "Telefonos"},
    
    {"store": "SoyTechno", "name": "iPhone 14 128GB", "price": "923.00", "category": "Telefonos"},
    {"store": "LatinBien", "name": "iPhone 14 (eSIM) 512GB", "price": "1484.65", "category": "Telefonos"},
    
    # Tablets
    {"store": "SoyTechno", "name": "Apple iPad mini 64GB", "price": "1096.00", "category": "Tablets"},
    {"store": "LatinBien", "name": "iPad mini - 7.9\" / 64GB", "price": "???", "category": "Tablets"},
    
    # Laptops
    {"store": "SoyTechno", "name": "All In One Lenovo IdeaCentre 23.8\" Ryzen 3", "price": "950.00", "category": "Computacion"},
    {"store": "LatinBien", "name": "???", "price": "???", "category": "Computacion"},
]

# Crear nuevas comparaciones
nuevos_matches = []
for i in range(0, len(nuevos_productos), 2):
    if i+1 < len(nuevos_productos):
        nuevos_matches.append([nuevos_productos[i], nuevos_productos[i+1]])

# Combinar con datos existentes
if "matches" not in data:
    data["matches"] = []

# Agregar nuevos matches
for match in nuevos_matches:
    data["matches"].append(match)

# Crear HTML
html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparacion de Precios - Merida</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }
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
        .no-matches { text-align: center; padding: 60px 20px; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Comparacion de Precios</h1>
            <p>Merida, Venezuela - LatinBien vs SoyTechno</p>
        </header>
        
        <div class="info-bar">
            <div><strong>Tiendas:</strong> LatinBien, SoyTechno</div>
            <div><strong>Comparaciones:</strong> <span id="total">""" + str(len(data.get("matches", []))) + """</span></div>
        </div>
        
        <div id="productGrid" class="product-grid"></div>
        
        <div id="noMatches" class="no-matches" style="display:none;">
            <h2>No se encontraron comparaciones</h2>
        </div>
    </div>

    <script>
        const data = """ + json.dumps(data) + """;
        
        function displayProducts() {
            const grid = document.getElementById('productGrid');
            const noMatches = document.getElementById('noMatches');
            
            if (!data.matches || data.matches.length === 0) {
                grid.innerHTML = '';
                noMatches.style.display = 'block';
                return;
            }
            
            noMatches.style.display = 'none';
            grid.innerHTML = '';
            
            data.matches.forEach(group => {
                const products = group.filter(p => p.store);
                if (products.length < 2) return;
                
                // Ordenar por precio
                const sorted = products.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                const minPrice = parseFloat(sorted[0].price);
                const maxPrice = parseFloat(sorted[sorted.length-1].price);
                const savings = maxPrice - minPrice;
                const savingsPct = ((savings / maxPrice) * 100).toFixed(1);
                
                const card = document.createElement('div');
                card.className = 'product-card';
                
                let pricesHTML = '';
                sorted.forEach(p => {
                    const price = parseFloat(p.price);
                    let rowClass = 'price-row';
                    if (price === minPrice) rowClass += ' best-price';
                    if (price === maxPrice && products.length > 1) rowClass += ' worst-price';
                    
                    pricesHTML += '<div class="' + rowClass + '"><span class="store-name">' + p.store + '</span><span class="price">$' + p.price + '</span></div>';
                });
                
                card.innerHTML = '<div class="product-header"><h3>' + products[0].name.substring(0, 60) + (products[0].name.length > 60 ? '...' : '') + '</h3><div>' + (products[0].category || 'Otros') + '</div></div><div class="price-comparison">' + pricesHTML + '</div>' + (savings > 0 ? '<div class="savings">Ahorro: <strong>$' + savings.toFixed(2) + '</strong> (' + savingsPct + '%)</div>' : '');
                
                grid.appendChild(card);
            });
        }
        
        displayProducts();
    </script>
</body>
</html>"""

# Guardar HTML
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comparacion_final.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML generado: {output_path}")
print(f"Total comparaciones: {len(data.get('matches', []))}")
