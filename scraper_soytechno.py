import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional


class SoyTechnoScraper:
    def __init__(self, base_url="https://soytechno.com"):
        self.base_url = base_url
        self.products = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_products(self, category_url=None):
        try:
            url = category_url if category_url else self.base_url
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            product_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/product/' in href or '/item/' in href:
                    full_url = href if href.startswith('http') else self.base_url + href
                    product_links.append(full_url)

            for link in set(product_links):
                product = self.scrape_product_page(link)
                if product:
                    self.products.append(product)
                time.sleep(1)

            return self.products

        except requests.RequestException as e:
            print(f"Error scraping products: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def scrape_product_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            product = {
                'url': url,
                'name': '',
                'price': None,
                'currency': 'DOP',
                'description': '',
                'availability': False
            }

            title_elem = soup.find('h1') or soup.find('h2')
            if title_elem:
                product['name'] = title_elem.get_text(strip=True)

            price_elem = soup.find(class_='price') or soup.find(class_='woocommerce-Price-amount')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_clean = ''.join(c for c in price_text if c.isdigit() or c == '.')
                try:
                    product['price'] = float(price_clean)
                except ValueError:
                    pass

            desc_elem = soup.find('div', class_='description') or soup.find('meta', {'name': 'description'})
            if desc_elem:
                if desc_elem.get('content'):
                    product['description'] = desc_elem['content']
                else:
                    product['description'] = desc_elem.get_text(strip=True)

            stock_elem = soup.find(class_='stock') or soup.find(class_='availability')
            if stock_elem:
                stock_text = stock_elem.get_text(strip=True).lower()
                product['availability'] = 'in stock' in stock_text or 'disponible' in stock_text

            return product

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error on {url}: {e}")
            return None

    def save_to_json(self, filename='soytechno_products.json'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(self.products)} products to {filename}")
            return True
        except IOError as e:
            print(f"Error saving to JSON: {e}")
            return False


if __name__ == '__main__':
    scraper = SoyTechnoScraper()
    products = scraper.scrape_products()
    scraper.save_to_json('soytechno_products.json')
