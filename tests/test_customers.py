import pytest


def test_create_customer(client):
    """Valida a API de criação de usuário."""
    payload = {
        'name': 'Luke Skywalwer',
        'email': 'luke_jedi@jedimail.force'
    }
    result = client.simulate_post('/customers', json=payload)

    assert result.status_code == 201, 'POST com sucesso retorna 201'
    assert result.json.get('name') == payload['name']


def test_email_must_be_unique(client):
    """Valida a regra de que o endereço de email deve ser único."""
    payload = {
        'name': 'Obi-Wan Kenobi',
        'email': 'kenobi.obi-wan@jedimail.force'
    }
    result = client.simulate_post('/customers', json=payload)
    assert result.status_code == 201

    payload = {
        'name': 'Yoda',
        'email': 'kenobi.obi-wan@jedimail.force'
    }
    result = client.simulate_post('/customers', json=payload)
    assert result.status_code == 400, 'O POST deve falhar se o email existir'
    data = result.json
    assert len(data) == 1, 'Somente o primeiro POST deve criar cliente'

    result = client.simulate_get('/customers')


def test_get_list_of_customers(client, customer):
    """Dado um cliente já criado, valida a API de listagem de clientes."""
    customer = customer
    result = client.simulate_get('/customers')
    assert result.status_code == 200

    data = result.json
    assert len(data) == 1, 'Somente um cliente foi criado'
    assert data[0]['name'] == customer.name
    assert data[0]['id'] == customer.id


def test_get_detail_of_customer(client, customer):
    """Dado um cliente já criado, validar a API de detalhes de um cliente."""
    customer = customer
    result = client.simulate_get(f'/customer/{customer.id}')
    assert result.status_code == 200

    data = result.json
    assert data['name'] == customer.name
    assert data['id'] == customer.id


def test_should_return_404_for_inexistent_customer(client, customer_anakin):
    """Dado um ID inválido, a API deve retornar 404."""
    result = client.simulate_get('/customer/99999')
    assert result.status_code == 404, 'ID 99999 não deve existir'
    assert result.json is None, 'Nenhum dado deve ser retornado'


def test_update_customer(client, customer_anakin):
    """Dado um cliente já criado, validar a API de update de clientes."""
    customer = customer_anakin
    url = f'/customer/{customer.id}'
    payload = {
        'name': 'Darth Vader',
        'email': 'lorde_vader@galactic_republic.gov'
    }

    # SQLAlchemy atualiza o objeto após o PUT
    customer_original_name = customer.name

    result = client.simulate_put(url, json=payload)
    assert result.status_code == 200

    data = result.json
    assert data['id'] == customer.id
    assert data['name'] != customer_original_name

    result = client.simulate_get(url)
    data = result.json

    assert result.status_code == 200
    assert data['id'] == customer.id
    assert data['name'] == payload['name']
    assert data['email'] == payload['email']


def test_cannot_update_to_an_existing_email(client, customer, customer_anakin):
    """Não deve ser possível alterar o email para um existente."""
    url = f'/customer/{customer.id}'
    payload = {
        'email': customer_anakin.email
    }

    result = client.simulate_get('/customers')
    assert isinstance(result.json, list)
    assert len(result.json) == 2

    result = client.simulate_put(url, json=payload)
    assert result.status_code == 400


def test_delete_customer(client, customer):
    url = f'/customer/{customer.id}'

    result = client.simulate_delete(url)
    assert result.status_code == 200

    result = client.simulate_get(url)
    assert result.status_code == 404
