from sqlalchemy import select
from models import *
from database import Session



#здесь будут функции конкретно для работы с бд


def get_user(last_name: str, first_name: str, middle_name: str):
    with Session() as session:
        query = select(Client).where(Client.last_name==last_name.capitalize()).where(Client.first_name==first_name.capitalize()).where(Client.middle_name==middle_name.capitalize())
        result = session.execute(query)
        return result.scalar_one()


def save(anything):
    with Session() as session:
        session.add(anything)
        session.commit()






