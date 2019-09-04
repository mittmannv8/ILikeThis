import pytest

from falcon import testing
from sqlalchemy import create_engine

from src import app
from src.db.manager import get_session, setup_database, drop_tables
from src.db.models import Customer


engine = create_engine('sqlite:///db_test.sqlite')
Session = get_session(engine)


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    """Helper que limpa a base de dados entre os testes."""
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(scope='session', autouse=True)
def setup_database_migration():
    """Executa as migrações no início dos testes."""
    drop_tables(engine)
    setup_database(engine)


@pytest.fixture()
def client(session):
    """Fixture para usar testar as chamadas de API do Falcon, usando a base de
    dados de teste."""
    return testing.TestClient(app.create_app(session))


@pytest.fixture(scope='function')
def customer_anakin(session):
    _customer = Customer(name='Anakin Skywalker',
                         email='fucking_jedi@jedimail.force')
    session.add(_customer)
    session.flush()
    return _customer


@pytest.fixture(scope='function')
def customer(session):
    _customer = Customer(name='Leia Organa',
                         email='rebel_princess@republic.gov')
    session.add(_customer)
    session.flush()
    return _customer
