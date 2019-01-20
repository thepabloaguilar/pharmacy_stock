from sqlalchemy import Column, Integer, String, Boolean, DateTime
from . import PostgresBase
from datetime import datetime

class Provider(PostgresBase):
    __tablename__ = 'provider'

    _id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    telephone = Column('telephone', String)
    is_active = Column('is_active', Boolean, default=True)
    creation_date = Column('creation_date', DateTime, default=datetime.now())
