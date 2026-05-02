import json

# Load LatinBien products
with open('latinbien_products.json', 'r', encoding='utf-8') as f:
    lb_data = json.load(f)

# Find bicycles in LatinBien
bicycles = [p for p in lb_data if 'bicicleta' in p['name'].lower() or 'bike' in p['name'].lower()]

print("Bicicletas REALES en LatinBien:")
for b in bicycles:
    print(f"  - {b['name']}: ${b['price']}")

# Check current verified comparison
with open('comparacion_verificada.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print("\nBicicletas en comparacion_verificada.json:")
for p in verified:
    if 'bicicleta' in p['nombre'].lower() or 'bike' in p['nombre'].lower():
        prices = [f"{x['tienda']}:${x['precio']}" for x in p['precios']]
        print(f"  - {p['nombre']}: {', '.join(prices)}")

print("\n---")
print("Ultrabikex.com no responde (timeout), no se pueden agregar comparaciones falsas")
print("Por ahora, las bicicletas solo mostraran el precio de LatinBien")
