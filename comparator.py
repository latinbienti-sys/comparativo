import json
import re
from difflib import get_close_matches

class PriceComparator:
    def __init__(self):
        self.all_products = []
        
    def load_products(self, *filenames):
        """Load products from JSON files"""
        for filename in filenames:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    products = json.load(f)
                    self.all_products.extend(products)
                    print(f"Loaded {len(products)} products from {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    def normalize_name(self, name):
        """Normalize product name for comparison"""
        # Remove special characters, convert to lowercase
        name = name.lower()
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name
    
    def find_similar_products(self, target_name, threshold=0.6):
        """Find similar products across all stores"""
        target_norm = self.normalize_name(target_name)
        target_words = set(target_norm.split())
        
        similar = []
        for product in self.all_products:
            product_norm = self.normalize_name(product['name'])
            product_words = set(product_norm.split())
            
            # Calculate similarity
            if target_words and product_words:
                intersection = target_words.intersection(product_words)
                union = target_words.union(product_words)
                similarity = len(intersection) / len(union) if union else 0
                
                if similarity >= threshold:
                    similar.append({
                        'product': product,
                        'similarity': similarity
                    })
        
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)
    
    def compare_by_category(self, category):
        """Compare all products in a category"""
        category_products = [p for p in self.all_products if p.get('category') == category]
        
        # Group by similar names
        groups = []
        processed = set()
        
        for i, product in enumerate(category_products):
            if i in processed:
                continue
                
            group = [product]
            processed.add(i)
            
            for j, other in enumerate(category_products):
                if j in processed or j == i:
                    continue
                    
                # Check similarity
                norm1 = self.normalize_name(product['name'])
                norm2 = self.normalize_name(other['name'])
                
                words1 = set(norm1.split())
                words2 = set(norm2.split())
                
                if words1 and words2:
                    intersection = words1.intersection(words2)
                    union = words1.union(words2)
                    similarity = len(intersection) / len(union)
                    
                    if similarity >= 0.5:
                        group.append(other)
                        processed.add(j)
            
            if len(group) > 1:
                groups.append(group)
        
        return groups
    
    def print_comparison(self, groups):
        """Print comparison results"""
        print("\n" + "="*80)
        print("COMPARACIÓN DE PRECIOS")
        print("="*80)
        
        for i, group in enumerate(groups, 1):
            print(f"\n## Grupo {i}: {group[0]['name'][:50]}...")
            print("-" * 60)
            
            # Sort by price
            sorted_group = sorted(group, key=lambda x: float(x['price']) if x['price'] else 999999)
            
            for product in sorted_group:
                print(f"  {product['store']:15} | ${product['price']:>10} | {product['name'][:40]}")
            
            # Calculate savings
            if len(sorted_group) > 1:
                prices = [float(p['price']) for p in sorted_group if p['price']]
                if prices:
                    min_price = min(prices)
                    max_price = max(prices)
                    savings = max_price - min_price
                    savings_pct = (savings / max_price * 100) if max_price > 0 else 0
                    print(f"  → Ahorro máximo: ${savings:.2f} ({savings_pct:.1f}%)")
    
    def generate_report(self, output_file='price_comparison_report.json'):
        """Generate a full comparison report"""
        categories = set(p.get('category', 'Otros') for p in self.all_products)
        
        report = {
            'summary': {
                'total_products': len(self.all_products),
                'stores': list(set(p['store'] for p in self.all_products)),
                'categories': list(categories)
            },
            'comparisons': {}
        }
        
        for category in categories:
            groups = self.compare_by_category(category)
            if groups:
                report['comparisons'][category] = [
                    {
                        'products': group,
                        'best_price': min(float(p['price']) for p in group if p['price']),
                        'worst_price': max(float(p['price']) for p in group if p['price']),
                        'savings': max(float(p['price']) for p in group if p['price']) - 
                                   min(float(p['price']) for p in group if p['price'])
                    }
                    for group in groups
                ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\nReport saved to {output_file}")
        return report

if __name__ == "__main__":
    comparator = PriceComparator()
    comparator.load_products('latinbien_products.json', 'multimax_products.json')
    
    # Generate comparison by category
    categories = set(p.get('category', 'Otros') for p in comparator.all_products)
    
    for category in categories:
        print(f"\nComparing category: {category}")
        groups = comparator.compare_by_category(category)
        comparator.print_comparison(groups)
    
    # Generate full report
    comparator.generate_report()
