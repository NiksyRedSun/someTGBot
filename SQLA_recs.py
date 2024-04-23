from sqlalchemy import select
from models import *
from database import Session


def get_user_by_last_name(last_name: str):
    with Session() as session:
        query = select(Client).where(Client.last_name==last_name.capitalize())
        result = session.execute(query)
        return result.scalar_one()




