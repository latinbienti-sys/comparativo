import json

# Load REAL LatinBien products from scraper
with open('latinbien_products.json', 'r', encoding='utf-8') as f:
    lb_data = json.load(f)

print(f"Total productos REALES scraped de LatinBien: {len(lb_data)}\n")

# Create normalized dictionary of LatinBien products
lb_dict = {}
for p in lb_data:
    # Normalize name: lowercase, remove quotes, extra spaces
    name = p['name'].lower().replace('"', '').replace('ñ', 'n').strip()
    while '  ' in name:
        name = name.replace('  ', ' ')
    lb_dict[name] = {
        'original_name': p['name'],
        'price': float(p['price']),
        'category': p.get('category', 'Otros')
    }

print("="*60)
print("PRODUCTOS REALES EN LATINBIEN:")
print("="*60)
for name, info in sorted(lb_dict.items()):
    print(f"  {info['original_name']}")
    print(f"     -> ${info['price']} | {info['category']}\n")

# Now check our verified comparison
with open('comparacion_verificada.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print("="*60)
print("VERIFICANDO CADA PRODUCTO EN COMPARACION_VERIFICADA.JSON:")
print("="*60)

clean_verified = []

for prod in verified:
    prod_name = prod['nombre'].lower().replace('"', '').replace('ñ', 'n').strip()
    while '  ' in prod_name:
        prod_name = prod_name.replace('  ', ' ')
    
    # Try to find match in LatinBien
    found = False
    matched_name = None
    
    for lb_name in lb_dict.keys():
        # Check if names are similar (contain same key words)
        prod_words = set(prod_name.split())
        lb_words = set(lb_name.split())
        
        # If more than 50% of words match, consider it a match
        if len(prod_words & lb_words) >= len(prod_words) * 0.5:
            found = True
            matched_name = lb_name
            break
    
    if found:
        real_price = lb_dict[matched_name]['price']
        print(f"✓ {prod['nombre']}")
        print(f"  -> ENCONTRADO en LatinBien: {lb_dict[matched_name]['original_name']}")
        print(f"  -> Precio real: ${real_price} | Precio en JSON: ${prod['precios'][0]['precio']}")
        
        # Update with REAL price
        new_precios = [p for p in prod['precios'] if p['tienda'] != 'LatinBien']
        new_precios.insert(0, {'tienda': 'LatinBien', 'precio': real_price})
        
        clean_verified.append({
            'nombre': lb_dict[matched_name]['original_name'],
            'categoria': lb_dict[matched_name]['category'],
            'precios': new_precios
        })
    else:
        print(f"✗ {prod['nombre']}")
        print(f"  -> NO EXISTE en LatinBien - REMOVIENDO\n")
        # Check if it has other stores
        other_stores = [p for p in prod['precios'] if p['tienda'] != 'LatinBien']
        if other_stores:
            print(f"  -> Se mantiene solo con otras tiendas: {[p['tienda'] for p in other_stores]}")
            clean_verified.append({
                'nombre': prod['nombre'],
                'categoria': prod['categoria'],
                'precios': other_stores
            })

print("\n" + "="*60)
print(f"RESULTADO: {len(clean_verified)} productos VERIFICADOS")
print("="*60)

# Save the truly clean version
with open('comparacion_100_verificada.json', 'w', encoding='utf-8') as f:
    json.dump(clean_verified, f, ensure_ascii=False, indent=4)

print("\nArchivo 'comparacion_100_verificada.json' creado")
print("Contiene SOLO productos que EXISTEN en LatinBien o tienen otras tiendas verificadas")
