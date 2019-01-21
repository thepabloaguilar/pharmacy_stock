from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from . import PostgresBase
from datetime import datetime
from .medicine_type import MedicineType

class Medicine(PostgresBase):
    __tablename__ = 'medicine'

    _id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    dosage = Column('dosage', Integer)
    amount = Column('amount', Numeric(16, 4))
    quantity = Column('quantity', Integer)
    provider_id = Column('provider_id', Integer, ForeignKey('provider.id'))
    medicine_type_id = Column('medicine_type_id', Integer, ForeignKey(MedicineType._id))
    is_active = Column('is_active', Boolean, default=True)
    creation_date = Column('creation_date', DateTime, default=datetime.now())
