from sqlalchemy import Column, Integer, String, Boolean, DateTime, CHAR
from . import PostgresBase
from datetime import datetime

class Customer(PostgresBase):
    __tablename__ = 'customer'

    _id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    telephone = Column('telephone', String)
    tax_id = Column('tax_id', String)
    is_active = Column('is_active', Boolean, default=True)
    genre = Column('genre', CHAR(1))
    creation_date = Column('creation_date', DateTime, default=datetime.now())
