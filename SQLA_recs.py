from sqlalchemy import select
from models import *
from database import Session



with Session() as session:
    query = select(Client)
    result = session.execute(query)
    print(result.scalar().id)



