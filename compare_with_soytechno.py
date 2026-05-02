import json
from difflib import SequenceMatcher


def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {filename}: {e}")
        return []


def calculate_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def compare_products(latinbien_products, soytechno_products, threshold=0.6):
    comparisons = []

    for latin_product in latinbien_products:
        latin_name = latin_product.get('name', '')
        best_match = None
        best_score = 0.0

        for soy_product in soytechno_products:
            soy_name = soy_product.get('name', '')
            score = calculate_similarity(latin_name, soy_name)

            if score > best_score and score >= threshold:
                best_score = score
                best_match = soy_product

        comparison = {
            'latinbien_product': latin_product,
            'soytechno_product': best_match,
            'similarity_score': best_score if best_match else 0.0,
            'price_difference': None
        }

        if best_match and latin_product.get('price') and best_match.get('price'):
            comparison['price_difference'] = latin_product['price'] - best_match['price']

        comparisons.append(comparison)

    return comparisons


def print_comparisons(comparisons):
    print("=" * 80)
    print("PRICE COMPARISON: LATINBIEN vs SOYTECHNO")
    print("=" * 80)

    for comp in comparisons:
        latin = comp['latinbien_product']
        soy = comp['soytechno_product']

        print(f"\nLatinBien: {latin.get('name', 'N/A')}")
        print(f"  Price: {latin.get('price', 'N/A')} {latin.get('currency', '')}")

        if soy:
            print(f"SoyTechno: {soy.get('name', 'N/A')}")
            print(f"  Price: {soy.get('price', 'N/A')} {soy.get('currency', '')}")
            print(f"  Similarity: {comp['similarity_score']:.2%}")
            if comp['price_difference'] is not None:
                diff = comp['price_difference']
                print(f"  Price Difference: {diff:+.2f}")
        else:
            print("  No matching product found")

    print("\n" + "=" * 80)


def save_comparisons(comparisons, filename='comparison_latinbien_soytechno.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(comparisons, f, ensure_ascii=False, indent=2)
        print(f"\nSaved comparisons to {filename}")
        return True
    except IOError as e:
        print(f"Error saving comparisons: {e}")
        return False


if __name__ == '__main__':
    latinbien_products = load_json('latinbien_products.json')
    soytechno_products = load_json('soytechno_products.json')

    if latinbien_products and soytechno_products:
        comparisons = compare_products(latinbien_products, soytechno_products)
        print_comparisons(comparisons)
        save_comparisons(comparisons, 'comparison_latinbien_soytechno.json')
    else:
        print("Cannot proceed without both product files.")
