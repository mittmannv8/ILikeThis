import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models

PROTOCOL = os.getenv('DATABASE_PROTOCOL', '')
HOST = os.getenv('DATABASE_HOST', 'localhost')
PORT = os.getenv('DATABASE_PORT', '5432')
NAME = os.getenv('DATABASE_NAME', '')
USER = os.getenv('DATABASE_USERNAME', '')
PASSWORD = os.getenv('DATABASE_PASSWORD', '')


engine = create_engine(
    (f'{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'),
    pool_size=100,
    echo=True
)


def get_session(engine=engine):
    return sessionmaker(bind=engine, autocommit=True)


def drop_tables(engine):
    """Helper para os testes."""
    models.Base.metadata.drop_all(engine)


def setup_database(engine=engine):
    migrate(engine)


def migrate(engine=engine):
    models.Base.metadata.create_all(engine)
