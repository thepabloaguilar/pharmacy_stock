import os

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

postgres_uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    os.getenv('POSTGRES_USER'),
    os.getenv('POSTGRES_PASSWORD'),
    os.getenv('POSTGRES_HOST'),
    os.getenv('POSTGRES_PORT'),
    os.getenv('POSTGRES_DB')
)

# Create connection engine with Postgres
postgres_db = create_engine(
    postgres_uri,
    poolclass=pool.NullPool,
    echo=True
)

# Object to create Database Sessions
PostgresSession = scoped_session(sessionmaker(bind=postgres_db))

# Object to map Database's Table
PostgresBase = declarative_base()
PostgresBase.metadata.bind = postgres_db
PostgresBase.query = PostgresSession.query_property()
