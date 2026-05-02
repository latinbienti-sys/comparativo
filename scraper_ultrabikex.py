import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_ultrabikex():
    """Scrape bicycle prices from Ultrabikex.com"""
    base_url = "https://ultrabikex.com/shop"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    bicycles = []
    
    try:
        print("Fetching Ultrabikex shop page...")
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product elements - adjust selectors based on actual page structure
        # Common patterns: product-item, product-card, product, etc.
        product_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(word in str(x).lower() for word in ['product', 'item', 'card']))
        
        print(f"Found {len(product_elements)} potential product elements")
        
        for elem in product_elements[:30]:  # Limit to first 30
            try:
                # Try to find product name
                name_elem = elem.find(['h2', 'h3', 'h4', 'a'], class_=lambda x: x and 'title' in str(x).lower())
                if not name_elem:
                    name_elem = elem.find('a')
                
                # Try to find price
                price_elem = elem.find(['span', 'div', 'p'], class_=lambda x: x and any(word in str(x).lower() for word in ['price', 'amount', 'cost']))
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    
                    # Extract price (remove currency symbols, dots, etc.)
                    price_clean = ''.join(c for c in price_text if c.isdigit() or c == '.')
                    try:
                        price = float(price_clean)
                        
                        # Only include if price seems reasonable for bicycles (over $100)
                        if price > 100:
                            bicycles.append({
                                'store': 'Ultrabikex',
                                'name': name,
                                'price': str(price),
                                'category': 'Deportes'
                            })
                            print(f"  Found: {name} - ${price}")
                    except ValueError:
                        pass
                        
            except Exception as e:
                print(f"  Error parsing element: {e}")
                continue
        
        # If no products found with above method, try alternative approach
        if not bicycles:
            print("\nTrying alternative parsing method...")
            # Look for any links that might be products
            links = soup.find_all('a', href=True)
            for link in links[:50]:
                text = link.get_text(strip=True)
                if any(word in text.lower() for word in ['bike', 'bici', 'spz', 'rockhopper', 'montaña', 'montana']):
                    print(f"  Potential product link: {text}")
        
        return bicycles
        
    except Exception as e:
        print(f"Error scraping Ultrabikex: {e}")
        return []

if __name__ == "__main__":
    print("Scraping Ultrabikex.com for bicycle prices...")
    bikes = scrape_ultrabikex()
    
    if bikes:
        with open('ultrabikex_bicycles.json', 'w', encoding='utf-8') as f:
            json.dump(bikes, f, ensure_ascii=False, indent=4)
        print(f"\nSaved {len(bikes)} bicycles to ultrabikex_bicycles.json")
    else:
        print("\nNo bicycles found. Site might use JavaScript or have different structure.")
        print("Let's try fetching the page content to analyze...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get("https://ultrabikex.com/shop", headers=headers, timeout=10)
            with open('ultrabikex_page.html', 'w', encoding='utf-8') as f:
                f.write(resp.text)
            print("Saved page to ultrabikex_page.html for analysis")
        except Exception as e:
            print(f"Could not fetch page: {e}")
