#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scraper_latinbien import LatinBienScraper

s = LatinBienScraper()
products = s.scrape_products(max_pages=1)
print(f'Found {len(products)} products')
for p in products[:5]:
    print(f'{p["name"]} - ${p["price"]}')
s.save_to_json()
