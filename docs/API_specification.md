## Documentação da API

### Autorização
A autorização é feita atráves de Token estático via headers.

```
Authorization: Token abc12
```

### GET /api/customers
Endpoint que retorna uma lista de clientes cadastrados.

**Response 200**

    [
      {
        "id": 1,
        "name": "Luke Skywalker",
        "email": "luke_jedi@jedimail.force"
      }
    ]

### POST /api/customers
Endpoint para cadastro de clientes.

**Payload**

    {
        "name": "Luke Skywalker",
        "email": "luke_jedi@jedimail.force"
    }

**Response 201**

    {
        "id": 1,
        "name": "Luke Skywalker",
        "email": "luke_jedi@jedimail.force"
    }

### GET /api/customer/{id}
Endpoint que retorna os detalhes de um cliente cadastrado.

**Response 200**

    {
        "id": 1,
        "name": "Luke Skywalker",
        "email": "luke_jedi@jedimail.force"
    }

### PUT /api/customer/{id}
Endpoint para atualizar os dados de um cliente cadastrado.

**Payload**

    {
        "name": "Luke Skywalker",
        "email": "skywalker.luke@jedimail.force"
    }

**Response 200**

    {
        "id": 1,
        "name": "Luke Skywalker",
        "email": "skywalker.luke@jedimail.force"
    }

### DELETE /api/customer/{id}
Endpoint para remover um cliente cadastrado.

**Response 200**

    No content

### GET /api/customer/{id}/products
Endpoint que retorna a lista de produtos favoritos de um cliente.

**Response 200**

    {
      "customer": 1,
      "products": [
        {
          "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
          "title": "R2-D2",
          "image": "http://robos.com/r2-d2.jpg",
          "price": 250000.0,
          "review": ""
        }
      ]
    }
        

### PUT /api/customer/{id}/products
Endpoint que insere um produto na lista de produtos favoritos de um cliente.

**Payload**

    {
        "product": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
    }

**Response 200**

        No content

### GET /api/customer/{id}/product/{uuid}
Endpoint que retorna os detalhes de um produto da lista de produtos favoritos de um cliente.

**Response 200**

    {
      "customer": 1,
      "product": {
          "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
          "title": "R2-D2",
          "image": "http://robos.com/r2-d2.jpg",
          "price": 250000.0,
          "review": ""
      }
    }

### DELETE /api/customer/{id}/product/{uuid}
Endpoint que remove um produto da lista de produtos favoritos de um cliente.

**Response 200**

    No content
