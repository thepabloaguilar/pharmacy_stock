from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from . import PostgresBase

class PharmacyUser(PostgresBase):
    __tablename__ = 'pharmacy_user'

    _id = Column('id', Integer, primary_key=True)
    username = Column('username', String)
    password = Column('password', String)
    is_active = Column('is_active', Boolean, default=True)
    is_admin = Column('is_admin', Boolean, default=False)
    creation_date = Column('creation_date', DateTime, default=datetime.now())
