import falcon


INSECURE_TOKEN = 'Token abc123'


class AuthMiddleware(object):
    """Middleware para autorização."""

    def process_request(self, request, response):
        token = request.get_header('Authorization')

        challenges = ['Token type="Static and Insecure"']

        if token is None:
            raise falcon.HTTPUnauthorized('Auth Token requerido',
                                          'Token não informado.',
                                          challenges)

        if not self._token_is_valid(token):
            raise falcon.HTTPUnauthorized('Authentication required',
                                          'Token inválido',
                                          challenges)

    def _token_is_valid(self, token):
        return token == INSECURE_TOKEN


class ORMSessionMiddleware:
    """Middleware que injeta uma sessão do ORM no resource."""

    def __init__(self, session):
        self.db_session = session

    def process_resource(self, request, response, resource, params):
        if request.method == 'OPTIONS':
            return

        resource.session = self.db_session

    def process_response(self, request, response, resource, request_succeeded):
        if request.method == 'OPTIONS':
            return

        db_session = getattr(self, 'session', None)

        if db_session:
            if not request_succeeded:
                db_session.rollback()
            db_session.close()
