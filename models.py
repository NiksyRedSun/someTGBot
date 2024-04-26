from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, Text, ForeignKey, Boolean, Float, Enum, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from typing import List
from database import Base
import datetime

#модели

class Client(Base):
    __tablename__ = "Clients"

    id = Column("Id", BigInteger, primary_key=True)
    first_name = Column("First Name", String)
    last_name = Column("Last Name", String)
    middle_name = Column("Middle Name", String)
    address = Column("Address", String)

    indicators: Mapped[List["Indicator"]] = relationship(back_populates="client")
    treatments: Mapped[List["Treatment"]] = relationship(back_populates="client")
    payments: Mapped[List["Payment"]] = relationship(back_populates="client")


class Indicator(Base):
    __tablename__ = "Indicators"

    id = Column("Id", Integer, primary_key=True)
    client_id = Column("ClientId", BigInteger, ForeignKey("Clients.Id", ondelete="CASCADE"))
    source = Column("Source", String)
    room_type = Column("RoomType", String)
    first_parameter = Column("FirstParameter", Integer)
    second_parameter = Column("SecondParameter", Integer)

    client = relationship(Client, back_populates='indicators')


class Treatment(Base):
    __tablename__ = "Treatments"

    id = Column("Id", Integer, primary_key=True)
    client_id = Column("ClientId", BigInteger, ForeignKey("Clients.Id", ondelete="CASCADE"))
    text = Column("Text", Text)
    type = Column("Type", String)


    client = relationship(Client, back_populates='treatments')


class Payment(Base):
    __tablename__ = "Payments"

    id = Column("Id", Integer, primary_key=True)
    client_id = Column("ClientId", BigInteger, ForeignKey("Clients.Id", ondelete="CASCADE"))
    sum = Column("Sum", Integer)
    created_date = Column("CreatedOn", DateTime, default=datetime.datetime.utcnow)

    client = relationship(Client, back_populates='payments')
