from sqlalchemy import Column, Integer, String
from . import PostgresBase

class MedicineType(PostgresBase):
    __tablename__ = 'medicine_type'

    _id = Column('id', Integer, primary_key=True)
    description = Column('description', String)
    unit = Column('unit', String)
