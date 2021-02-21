import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Numeric, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import psycopg2
from settings import DB_URI,DB_TABLE

# Connect to Postgres database 
Base = declarative_base()
engine = create_engine(DB_URI)

class MovieModel(Base):
   __tablename__ = DB_TABLE
   __table_args__ = {'extend_existing': True} 
   id = Column(Integer,primary_key=True, unique=True)
   title = Column(String,nullable=True)
   year = Column(Integer)
   budget = Column(Numeric)
   revenue = Column(Numeric)
   ratio = Column(Numeric)
   rating = Column(Numeric)
   production_company = Column(String)
   wiki_link = Column(String)
   wiki_abstract = Column(String)
   created_at = Column(DateTime(), server_default=func.now())
 
Session = sessionmaker(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

  