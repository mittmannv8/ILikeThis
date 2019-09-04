import logging

import falcon
from sqlalchemy.exc import IntegrityError
from ilikedthis.db.models import Customer


def customer_serializer(customer):
    """Serializer para objetos do tipo Customer."""
    return {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email
    }


class CustomersResource(object):
    """Resource responsável pelos endpoints de listagem e criação."""

    def on_get(self, request, response):
        customers = self.session.query(Customer)
        response.media = [customer_serializer(c) for c in customers]


    def on_post(self, request, response):
        try:
            data = request.media
            customer = Customer(name=data['name'], email=data['email'])
            self.session.add(customer)
            self.session.flush()

        except (AttributeError, KeyError, IntegrityError):
            raise falcon.HTTPBadRequest()

        response.status = falcon.HTTP_201
        response.media = customer_serializer(customer)

class CustomerResource:
    """Resource responsável pelos endpoints de detalhe, delete e update."""

    def _get_customer(self, customer_id):
        """Helper para consultar um customer pelo ID."""
        customer = (
            self.session
            .query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise falcon.HTTPNotFound()

        return customer

    def on_get(self, request, response, customer_id):
        customer = self._get_customer(customer_id)
        response.media = customer_serializer(customer)

    def on_put(self, request, response, customer_id):
        try:
            data = request.media
            customer = self._get_customer(customer_id)
            customer.name = data.get('name', customer.name)
            customer.email = data.get('email', customer.email)
            self.session.merge(customer)
            response.media = customer_serializer(customer)
        except Exception as e:
            logging.exception('An error occurred on update customer %s: %s',
                              customer_id, e)
            raise falcon.HTTPBadRequest()

    def on_delete(self, request, response, customer_id):
        try:
            customer = self._get_customer(customer_id)
            self.session.delete(customer)
        except Exception as e:
            logging.exception('An error occurred on update customer %s: %s',
                              customer_id, e)
            raise falcon.HTTPBadRequest()
