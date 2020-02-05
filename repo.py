# репозиторий для работы с БД
import os
from builtins import str
from typing import Dict

import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import FlushError

from models import Person, Order, Base



class Repo(object):
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        #connStr = 'mysql+mysqlconnector://root:Ujvbhrf1557@localhost:3306/botdb'
        self.connStr = 'sqlite:///' + os.path.join(basedir, 'app.db')
        self.engine = create_engine(self.connStr, echo=False)
        #Session = sessionmaker(bind=self.engine)
        self.session = self.create_session(self.engine)
        self.recreate_database()

    def create_session(self, engine) -> sqlalchemy.orm.Session:
        Session = sqlalchemy.orm.sessionmaker(expire_on_commit=False)
        Session.configure(bind=engine)
        session: sqlalchemy.orm.Session = Session()
        return session

    def session_commit(self) -> bool:
        ok: bool = True
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            ok = False
        except FlushError:
            ok = False
        return ok

    def recreate_database(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def add_user(self, line: str) -> Dict:
        person = Person.from_string(line)
        self.session.add(person)
        ok: bool = self.session_commit()
        return {'ok':ok, 'person':person}

repo = Repo();
str = "email=ohmanyukov@mail.ru;id=None; is_customer=True; is_performer=False; name=Ольга Охманюк; phone=+79246432292"
result = repo.add_user(str)
print(result['person'])
