import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

class LatinBienScraper:
    def __init__(self):
        self.base_url = "https://latinbien.com"
        self.shop_url = f"{self.base_url}/shop"
        self.products = []
        
    def scrape_products(self, max_pages=3):
        """Scrape products from LatinBien"""
        print("Scraping LatinBien...")
        
        for page in range(1, max_pages + 1):
            url = f"{self.shop_url}/page/{page}" if page > 1 else self.shop_url
            print(f"  Fetching page {page}...")
            
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find product containers (Odoo standard class)
                product_elements = soup.find_all('div', class_='o_wsale_product_grid')
                
                if not product_elements:
                    # Fallback: find all product template images
                    product_elements = soup.find_all('img', src=lambda x: x and 'product.template' in x)
                    product_elements = [img.find_parent('div', class_=lambda x: x and 'col' in x.lower()) for img in product_elements if img.find_parent('div')]
                    product_elements = [x for x in product_elements if x is not None]
                
                print(f"    Found {len(product_elements)} product elements")
                
                for elem in product_elements:
                    product = self._extract_product(elem)
                    if product:
                        self.products.append(product)
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                print(f"  Error on page {page}: {e}")
                break
                
        return self.products
    
    def _extract_product(self, elem):
        """Extract product info from element"""
        try:
            # Find the product link (contains /shop/ in href)
            product_link = elem.find('a', href=lambda x: x and '/shop/' in x and 'product' not in str(x))
            if not product_link:
                product_link = elem.find('a', href=lambda x: x and '/shop/' in x)
            
            # Name from the link text or heading
            name = ""
            if product_link:
                name = product_link.get_text(strip=True)
            
            # If no name from link, try headings
            if not name:
                for tag in ['h6', 'h5', 'h4', 'h3', 'strong']:
                    name_elem = elem.find(tag)
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        break
            
            # Price - look for text containing "$" and numbers
            import re
            price = ""
            elem_text = elem.get_text()
            
            # Pattern: $ 2.369,34 2369.34 USD or similar
            price_patterns = [
                r'\$\s*([\d.,]+)\s*\d+\.\d+\s*USD',
                r'Precio.*?\$\s*([\d.,]+)',
                r'\$\s*([\d.,]+)',
                r'(\d+\.\d+)\s*USD'
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, elem_text)
                if match:
                    price_str = match.group(1) if match.lastindex else match.group(0)
                    # Clean and convert to standard format
                    price_str = price_str.replace('.', '').replace(',', '.')
                    price_match = re.search(r'\d+\.?\d*', price_str)
                    if price_match:
                        price = price_match.group()
                        break
            
            # URL
            product_url = ""
            if product_link and product_link.get('href'):
                product_url = urljoin(self.base_url, product_link['href'])
            
            # Image
            img_elem = elem.find('img', src=True)
            img_url = urljoin(self.base_url, img_elem['src']) if img_elem else ""
            
            if name and price:
                return {
                    'store': 'LatinBien',
                    'name': name,
                    'price': price,
                    'url': product_url,
                    'image': img_url,
                    'category': self._detect_category(name)
                }
        except Exception as e:
            pass
        return None
    
    def _detect_category(self, name):
        """Simple category detection based on product name"""
        name_lower = name.lower()
        if any(x in name_lower for x in ['iphone', 'samsung', 'xiaomi', 'honor', 'celular', 'phone']):
            return 'Telefonos'
        elif any(x in name_lower for x in ['tv', 'televisor', 'smart tv']):
            return 'Televisores'
        elif any(x in name_lower for x in ['laptop', 'notebook', 'computadora']):
            return 'Computacion'
        elif any(x in name_lower for x in ['aire', 'acondicionado']):
            return 'Hogar'
        elif any(x in name_lower for x in ['nevera', 'refrigerador']):
            return 'Hogar'
        elif any(x in name_lower for x in ['lavadora']):
            return 'Hogar'
        return 'Otros'
    
    def save_to_json(self, filename='latinbien_products.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.products)} products to {filename}")

if __name__ == "__main__":
    scraper = LatinBienScraper()
    products = scraper.scrape_products(max_pages=2)
    scraper.save_to_json()
