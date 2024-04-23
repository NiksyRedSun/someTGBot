from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from config import USERNAME, PASSWORD, DB_NAME


url_object = URL.create(
    "postgresql",
    username=USERNAME,
    password=PASSWORD,
    host="localhost",
    database=DB_NAME,
)

engine = create_engine(url_object)

Session = sessionmaker(bind=engine)








