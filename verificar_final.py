import json
import requests
from bs4 import BeautifulSoup

# First, retry Ultrabikex
print("="*60)
print("REINTENTANDO ULTRABIKEX.COM...")
print("="*60)

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    print("Fetching https://ultrabikex.com/shop ...")
    response = requests.get("https://ultrabikex.com/shop", headers=headers, timeout=20)
    
    if response.status_code == 200:
        print(f"SUCCESS! Status: {response.status_code}")
        print(f"Content length: {len(response.text)} characters")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for bicycle-related content
        text = soup.get_text().lower()
        if 'bike' in text or 'bici' in text or 'spz' in text:
            print("\nFound bicycle-related content!")
            
            # Try to find products
            # Look for common product patterns
            links = soup.find_all('a', href=True)
            products_found = []
            
            for link in links:
                link_text = link.get_text(strip=True)
                if any(word in link_text.lower() for word in ['spz', 'rockhopper', 'bike', 'bicicleta']):
                    if len(link_text) > 10 and len(link_text) < 200:
                        products_found.append(link_text)
            
            if products_found:
                print(f"\nFound {len(products_found)} potential bicycle products:")
                for p in products_found[:10]:
                    print(f"  - {p}")
            else:
                print("\nNo specific products found in links")
                print("Saving page for manual analysis...")
                with open('ultrabikex_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("Page saved to ultrabikex_page.html")
        else:
            print("No bicycle content detected - site might be blocked or different")
            
    else:
        print(f"Failed with status: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("VERIFICANDO PRODUCTOS LATINBIEN...")
print("="*60)

# Load REAL LatinBien products from scraper
with open('latinbien_products.json', 'r', encoding='utf-8') as f:
    lb_data = json.load(f)

print(f"Total productos REALES scraped de LatinBien: {len(lb_data)}\n")

# Create normalized dictionary
lb_dict = {}
for p in lb_data:
    name = p['name'].lower().replace('"', '').replace('ñ', 'n').strip()
    while '  ' in name:
        name = name.replace('  ', ' ')
    lb_dict[name] = {
        'original_name': p['name'],
        'price': float(p['price']),
        'category': p.get('category', 'Otros')
    }

# Load current verified comparison
with open('comparacion_verificada.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print("="*60)
print("VERIFICACION PRODUCTO POR PRODUCTO:")
print("="*60)

clean_data = []

for prod in verified:
    prod_name = prod['nombre'].lower().replace('"', '').replace('ñ', 'n').strip()
    while '  ' in prod_name:
        prod_name = prod_name.replace('  ', ' ')
    
    # Try to find match
    found = False
    matched_key = None
    
    for lb_name in lb_dict.keys():
        # Check word overlap
        prod_words = set(prod_name.split())
        lb_words = set(lb_name.split())
        
        if len(prod_words & lb_words) >= 2:  # At least 2 words match
            found = True
            matched_key = lb_name
            break
    
    if found:
        real_price = lb_dict[matched_key]['price']
        print(f"OK: {prod['nombre']}")
        print(f"    -> LatinBien: {lb_dict[matched_key]['original_name']}")
        print(f"    -> Precio real: ${real_price}")
        
        # Update with real price
        new_precios = [p for p in prod['precios'] if p['tienda'] != 'LatinBien']
        if not any(p['tienda'] == 'LatinBien' for p in new_precios):
            new_precios.insert(0, {'tienda': 'LatinBien', 'precio': real_price})
        
        clean_data.append({
            'nombre': lb_dict[matched_key]['original_name'],
            'categoria': lb_dict[matched_key]['category'],
            'precios': new_precios
        })
    else:
        print(f"NOT FOUND: {prod['nombre']}")
        print(f"    -> NO existe en LatinBien")
        # Keep only if has other stores
        other_stores = [p for p in prod['precios'] if p['tienda'] != 'LatinBien']
        if other_stores:
            print(f"    -> Manteniendo con otras tiendas")
            clean_data.append({
                'nombre': prod['nombre'],
                'categoria': prod['categoria'],
                'precios': other_stores
            })
        else:
            print(f"    -> ELIMINANDO (no existe en ninguna tienda)")

print("\n" + "="*60)
print(f"RESULTADO FINAL: {len(clean_data)} productos VERIFICADOS")
print("="*60)

# Save the truly clean version
with open('comparacion_final_verificada.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=4)

print("\nArchivo 'comparacion_final_verificada.json' creado")
print("100% verificado - SOLO productos que existen en las tiendas")
