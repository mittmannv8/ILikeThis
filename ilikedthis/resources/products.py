import falcon

from ilikedthis.db.models import Customer, Favorite
from ilikedthis.services.products import get_products_details


class ProductResourceBase:

    def get_customer_by_id(self, customer_id):
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

    def get_favorite_product_from_id_and_customer(self, customer, product_id):
        """Helper para consultar um produto dentro da lista de favoritos."""
        return (
            self.session
            .query(Favorite)
            .filter(Favorite.product == product_id,
                    Favorite.customer_id == customer.id)
            .first()
        )

    def serialize_response(self, customer, products, many=False):
        serialized = {
            'customer': customer.id
        }

        if many:
            serialized['products'] = get_products_details(products)
        else:
            details = get_products_details([products])
            serialized['product'] = details[0] if details else {}

        return serialized


class ProductsResource(ProductResourceBase):

    def on_get(self, request, response, customer_id):
        customer = self.get_customer_by_id(customer_id)
        products = customer.favorites[:10]

        response.media = self.serialize_response(customer, products, many=True)

    def on_put(self, request, response, customer_id):
        """Insere produtos na lista de favoritos do usuário."""
        customer = self.get_customer_by_id(customer_id)

        product = request.media.get('product')
        already_add = self.get_favorite_product_from_id_and_customer(
            customer, product)

        if already_add:
            raise falcon.HTTPBadRequest()

        customer.favorites.append(Favorite(product=product))
        response.status_code = falcon.HTTP_201


class ProductResource(ProductResourceBase):

    def on_get(self, request, response, customer_id, product_id):
        customer = self.get_customer_by_id(customer_id)
        product = self.get_favorite_product_from_id_and_customer(
            customer, product_id)
        if not product:
            raise falcon.HTTPNotFound()

        response.media = self.serialize_response(customer, product)

    def on_delete(self, request, response, customer_id, product_id):
        customer = self.get_customer_by_id(customer_id)
        product = self.get_favorite_product_from_id_and_customer(
            customer, product_id)
        self.session.delete(product)
