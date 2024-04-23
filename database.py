from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from config import DB_HOST, DB_PASS, DB_USER, DB_PORT, DB_NAME


url_object = URL.create(
    "postgresql",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)


engine = create_engine(url_object)

Session = sessionmaker(bind=engine)

Base = declarative_base()





