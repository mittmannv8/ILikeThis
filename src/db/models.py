from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)

    favorites = relationship('Favorite')

    def __repr__(self):
        return f'<Customer {self.id}: {self.email}>'


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True)
    product = Column(String(36))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    def __repr__(self):
        return f'<Favorite {self.product}: {self.product}>'
