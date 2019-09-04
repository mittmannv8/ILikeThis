import falcon

from .db.manager import get_session
from .middlewares import AuthMiddleware, ORMSessionMiddleware
from .resources import customers, products


class HealthResource(object):
    def on_get(self, request, response):

        response.status = falcon.HTTP_200
        response.body = json.dumps({
            'status': 'ok'
        })


def create_app(session=None):
    # WSGI
    session = session or get_session()
    api = falcon.API(middleware=[AuthMiddleware(),
                                 ORMSessionMiddleware(session),])

    # Resources
    api.add_route('/health', HealthResource())
    api.add_route('/api/customers', customers.CustomersResource())
    api.add_route('/api/customer/{customer_id}', customers.CustomerResource())
    api.add_route('/api/customer/{customer_id}/products',
                  products.ProductsResource())
    api.add_route('/api/customer/{customer_id}/product/{product_id}',
                  products.ProductResource())
    return api
