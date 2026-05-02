import requests
from bs4 import BeautifulSoup
import json
import time

class MultimaxScraper:
    def __init__(self):
        self.base_url = "https://multimax.com.ve"
        self.products = []
        
    def scrape_products(self):
        """Scrape products from Multimax"""
        print("Scraping Multimax...")
        
        # Main categories to scrape
        categories = [
            "/producto/lavadora-automatica-frigidaire-24kg/",
            "/producto/",
        ]
        
        # Try to get product listing pages
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product links
            product_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/producto/' in href and href not in product_links:
                    product_links.append(href)
            
            print(f"  Found {len(product_links)} product links")
            
            for link in product_links[:20]:  # Limit to 20 products for testing
                product = self._scrape_product_page(link)
                if product:
                    self.products.append(product)
                time.sleep(0.5)
                
        except Exception as e:
            print(f"  Error: {e}")
            
        return self.products
    
    def _scrape_product_page(self, path):
        """Scrape individual product page"""
        try:
            url = f"{self.base_url}{path}" if not path.startswith('http') else path
            print(f"    Fetching {url}")
            
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Name
            name_elem = soup.find('h1') or soup.find('h2', {'class': 'product_title'})
            name = name_elem.get_text(strip=True) if name_elem else ""
            
            # Price
            price_elem = soup.find('span', {'class': 'price'}) or soup.find('bdi')
            price = ""
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    price = price_match.group()
            
            if name and price:
                return {
                    'store': 'Multimax',
                    'name': name,
                    'price': price,
                    'url': url,
                    'category': self._detect_category(name)
                }
        except Exception as e:
            print(f"      Error: {e}")
            pass
        return None
    
    def _detect_category(self, name):
        """Detect category from product name"""
        name_lower = name.lower()
        if any(x in name_lower for x in ['celular', 'iphone', 'samsung', 'xiaomi']):
            return 'Telefonos'
        elif any(x in name_lower for x in ['tv', 'televisor', 'smart']):
            return 'Televisores'
        elif any(x in name_lower for x in ['laptop', 'notebook']):
            return 'Computacion'
        elif any(x in name_lower for x in ['lavadora', 'secadora', 'nevera', 'aire']):
            return 'Hogar'
        return 'Otros'
    
    def save_to_json(self, filename='multimax_products.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.products)} products to {filename}")

if __name__ == "__main__":
    scraper = MultimaxScraper()
    products = scraper.scrape_products()
    scraper.save_to_json()
