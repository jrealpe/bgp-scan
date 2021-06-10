from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5433/db_scan')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
