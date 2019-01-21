from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from . import PostgresBase

class Sale(PostgresBase):
    __tablename__ = 'sale'

    _id = Column('id', Integer, primary_key=True)
    amount = Column('amount', Numeric(16, 4))
    transaction_date = Column('transaction_date', DateTime)
    customer_id = Column('customer_id', Integer, ForeignKey('customer.id'))
    seller_id = Column('seller_id', Integer, ForeignKey('pharmacy_user.id'))
    status = Column('status', String, default='PENDING')
    creation_date = Column('creation_date', DateTime, default=datetime.now())
