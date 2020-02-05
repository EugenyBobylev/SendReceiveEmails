# Описание модели БД
from typing import Dict, List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import json

Base = declarative_base()


def str_to_dict(data_str: str, dict_split=";", item_split="=") -> Dict:
    pairs: List[str] = data_str.split(dict_split)
    for i in range(len(pairs)):
        pairs[i] = pairs[i].strip()  # удалить проеблы
        pairs[i] = pairs[i].split(item_split)
    d = {k: v for (k, v) in pairs}
    return d


class Person(Base):
    __tablename__ = 'persons'

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(128), nullable=False)
    email = Column("Email", String(128))
    phone = Column("Phone", String(64))
    is_customer = Column("IsCustomer", Boolean, default=False)
    is_performer = Column("IsPerformer", Boolean, default=False)

    customer_orders = relationship("Order", foreign_keys='Order.id_customer', back_populates="customer", lazy=False)
    performer_orders = relationship("Order", foreign_keys='Order.id_performer', back_populates="performer", lazy=False)

    def __init__(self):
        self.id = None
        self.name = ''
        self.email = ''
        self.phone = ''
        self.is_customer = False
        self.is_performer = False

    def __repr__(self):
        return f'id={self.id}; name={self.name}; email={self.email}; phone={self.phone}'

    def from_string(line: str) -> 'Person':
        def parse(key: str):
            if key in data:
                return data[key]
            else:
                return None

        def str_to_int(value: str):
            if value is None:
                return None
            result = None
            try:
                result = int(value)
            except ValueError:
                pass
            return result

        data = str_to_dict(line)
        person = Person()
        person.id = str_to_int(parse('id'))
        person.name = parse('name')
        person.email = parse('email')
        person.phone = parse('phone')
        person.is_customer = parse('is_customer') == 'True'
        person.is_performer = parse('is_performer') == 'True'
        return person


class Order(Base):
    __tablename__ = "orders"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    id_customer = Column("IdCustomer", Integer, ForeignKey("persons.Id"))
    id_performer = Column("IdPerformer", Integer, ForeignKey("persons.Id"))
    url_source = Column("UrlSource", String(255), nullable=False)
    url_result = Column("UrlResult", String(255))

    customer = relationship("Person", foreign_keys=[id_customer])
    performer = relationship("Person", foreign_keys=[id_performer])

    def __repr__(self):
        return f'id={self.id}; customer={self.customer}; performer={self.performer}' \
               f'url_spurce={self.url_source}; url_result={self.url_result}'


