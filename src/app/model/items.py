from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Items(Base):
    """ Set of items being tracked"""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column('item_name', String, nullable=False)
    price = Column('price', Integer, nullable=False)

    UniqueConstraint('item_name')
