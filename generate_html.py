#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un archivo HTML con los datos de comparacion embebidos
"""

import json

# Cargar datos
try:
    with open('quick_comparison.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    data = {"matches": [], "latinbien_count": 0}

# Cargar productos individuales para mas detalles
try:
    with open('latinbien_products.json', 'r', encoding='utf-8') as f:
        latinbien = json.load(f)
except:
    latinbien = []

try:
    with open('soytechno_products.json', 'r', encoding='utf-8') as f:
        soytechno = json.load(f)
except:
    soytechno = []

# Crear HTML
html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparacion de Precios - Merida</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .info-bar {
            background: #f8f9fa;
            padding: 15px 30px;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            padding: 30px;
        }
        .product-card {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            border-color: #667eea;
        }
        .product-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }
        .product-header h3 {
            font-size: 1.3em;
            margin-bottom: 5px;
        }
        .price-comparison {
            padding: 20px;
        }
        .price-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .price-row.best-price {
            background: #d4edda;
            border: 2px solid #28a745;
            font-weight: bold;
        }
        .price-row.worst-price {
            background: #f8d7da;
            border: 2px solid #dc3545;
        }
        .store-name {
            font-weight: 600;
            color: #495057;
        }
        .price {
            font-size: 1.3em;
            font-weight: bold;
            color: #667eea;
        }
        .best-price .price {
            color: #28a745;
        }
        .worst-price .price {
            color: #dc3545;
        }
        .savings {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 15px;
            margin: 10px 20px;
            border-radius: 8px;
            text-align: center;
        }
        .no-matches {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Comparacion de Precios</h1>
            <p>Merida, Venezuela - LatinBien vs Competencia</p>
        </header>
        
        <div class="info-bar">
            <div><strong>Tiendas:</strong> LatinBien, Multimax, MegaTecno</div>
            <div><strong>Productos:</strong> """ + str(len(latinbien)) + """ en LatinBien</div>
        </div>
        
        <div id="productGrid" class="product-grid"></div>
        
        <div id="noMatches" class="no-matches" style="display:none;">
            <h2>No se encontraron comparaciones</h2>
        </div>
    </div>

    <script>
        const data = """ + json.dumps(data) + """;
        const latinbien = """ + json.dumps(latinbien[:20]) + """;
        
        function displayProducts() {
            const grid = document.getElementById('productGrid');
            const noMatches = document.getElementById('noMatches');
            
            let matches = [];
            
            // Usar datos de comparacion si existen
            if (data.matches && data.matches.length > 0) {
                matches = data.matches;
            } else {
                // Crear comparaciones simples
                matches = latinbien.map(p => [p]);
            }
            
            if (matches.length === 0) {
                grid.innerHTML = '';
                noMatches.style.display = 'block';
                return;
            }
            
            noMatches.style.display = 'none';
            grid.innerHTML = '';
            
            matches.forEach(group => {
                const products = group.filter(p => p.store);
                if (products.length === 0) return;
                
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
                    
                    pricesHTML += `
                        <div class="${rowClass}">
                            <span class="store-name">${p.store}</span>
                            <span class="price">$${p.price}</span>
                        </div>
                    `;
                });
                
                card.innerHTML = `
                    <div class="product-header">
                        <h3>${products[0].name.substring(0, 60)}${products[0].name.length > 60 ? '...' : ''}</h3>
                        <div>${products[0].category || 'Otros'}</div>
                    </div>
                    <div class="price-comparison">
                        ${pricesHTML}
                    </div>
                    ${savings > 0 ? `
                        <div class="savings">
                            Ahorro: <strong>$${savings.toFixed(2)}</strong> (${savingsPct}%)
                        </div>
                    ` : ''}
                `;
                
                grid.appendChild(card);
            });
        }
        
        displayProducts();
    </script>
</body>
</html>"""

import os
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comparacion_final.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML generado: {output_path}")
print(f"Total de coincidencias: {len(data.get('matches', []))}")
