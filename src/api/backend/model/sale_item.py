from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, Numeric, ForeignKey
from . import PostgresBase

class SaleItem(PostgresBase):
    __tablename__ = 'sale_item'

    _id = Column('id', Integer, primary_key=True)
    sale_id = Column('sale_id', Integer, ForeignKey('sale.id'))
    medicine_id = Column('medicine_id', Integer, ForeignKey('medicine.id'))
    current_medicine_price = Column('current_medicine_price', Numeric(16, 4))
    quantity = Column('quantity', Integer)
    final_price = Column('final_price', Numeric(16, 4))
    is_cancelled = Column('is_cancelled', Boolean, default=False)
    creation_date = Column('creation_date', DateTime, default=datetime.now())
