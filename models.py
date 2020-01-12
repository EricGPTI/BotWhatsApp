from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


engine = create_engine('db_mysql', encoding='utf8', echo=True)
BASE = declarative_base()



