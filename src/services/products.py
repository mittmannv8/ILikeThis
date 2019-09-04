import requests


def get_product_details(product):
    """Consulta a API de produtos para serializar a API de favoritos."""
    url = f'http://challenge-api.luizalabs.com/api/product/{product.product}'
    response = requests.get(url)

    try:
        data = response.json()
        return {
            'id': data.get('id', ''),
            'title': data.get('title', ''),
            'image': data.get('image', ''),
            'price': data.get('price', ''),
            'review': data.get('reviewScore', '')
        }
    except:
        return {}


def get_products_details(products):
    return [get_product_details(p) for p in products]
