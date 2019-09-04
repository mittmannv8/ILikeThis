import pytest
from unittest import mock

from src.db.models import Favorite

PRODUCTS_EXTERNAL_API = [
    {
        "price": 1360000.0,
        "image": "https://picsum.photos/200",
        "brand": "Ralph McQuarrie",
        "id": "220a2242-dc18-4b73-b891-e089840fa6ac",
        "title": "Astromech Droid R2-D2 model"
    },
    {
        "price": 1100000.0,
        "image": "https://picsum.photos/200",
        "brand": "Anakin Skywalker",
        "id": "c908d750-bf6a-4432-9e15-89150720835f",
        "title": "C-3PO Protocol Droid gold version"
    }
]


def setup_module(module):
    # cria um mock para o restorno da API externa
    requests = mock.patch('src.services.products.requests.get')
    mock_start = requests.start()
    mock_start.return_value.json.return_value = PRODUCTS_EXTERNAL_API[0]


@pytest.fixture()
def favorite(session, customer):
    """Add um produto a lista de favoritos de customer."""
    product = PRODUCTS_EXTERNAL_API[0]
    _favorite = Favorite(product=product['id'])
    customer.favorites.append(_favorite)
    session.flush()
    return _favorite


def test_get_product_list(client, customer, favorite):
    result = client.simulate_get(f'/customer/{customer.id}/products')
    assert result.status_code == 200

    data = result.json
    product_api = data['products'][0]
    product_external = PRODUCTS_EXTERNAL_API[0]

    assert product_api['id'] == product_external['id']
    assert product_api['title'] == product_external['title']

    assert set(product_api.keys()) == set(('id', 'title', 'image', 'price',
                                           'review'))


def test_should_return_empty_list_for_new_user(client, customer):
    result = client.simulate_get(f'/customer/{customer.id}/products')
    assert result.status_code == 200
    data = result.json
    assert isinstance(data['products'], list)
    assert data['products'] == []


def test_insert_product_in_an_inexistent_favorite_list(client, customer):
    url = f'/customer/{customer.id}/products'

    payload = {
        'product': PRODUCTS_EXTERNAL_API[0]['id'],
    }
    result = client.simulate_put(url, json=payload)
    assert result.status_code == 200

    result = client.simulate_get(url)
    assert result.status_code == 200
    data = result.json
    assert len(data['products']) == 1
    assert data['customer'] == customer.id
    assert data['products'][0]['id'] == payload['product']


def test_should_product_unique_in_customer_list(client, customer, favorite):
    assert len(customer.favorites) == 1, 'customer must have an product to test'

    url = f'/customer/{customer.id}/products'
    payload = {
        'product': favorite.product
    }
    result = client.simulate_put(url, json=payload)
    assert result.status_code == 400

    result = client.simulate_get(url)
    assert result.status_code == 200
    data = result.json
    assert len(data['products']) == 1


def test_get_details_of_favorite_product(client, customer, favorite):
    url = f'/customer/{customer.id}/product/{favorite.product}'
    result = client.simulate_get(url)
    assert result.status_code == 200
    data = result.json
    assert data['customer'] == customer.id
    assert data['product']['id'] == PRODUCTS_EXTERNAL_API[0]['id']


def test_remove_product_from_favorite_list(client, customer, favorite):
    url = f'/customer/{customer.id}/product/{favorite.product}'
    result = client.simulate_delete(url)
    assert result.status_code == 200

    result = client.simulate_get(url)
    assert result.status_code == 404
