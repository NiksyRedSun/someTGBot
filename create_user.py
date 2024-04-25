from sqlalchemy import select
from models import *
from database import Session



user = Client(id=1211235, first_name="Сергей", last_name="Кирилов", middle_name="Владимирович", address='г. Анапа, ул. Ленина, д. 45, кв.  77')


try:
    with Session() as session:
        session.add(user)
        session.commit()
        print("Пользователь создан")
except:
    print("Пользователь не создан, что-то пошло не так")


input("Нажмите ENTER для продолжения")