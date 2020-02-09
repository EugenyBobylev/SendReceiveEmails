# репозиторий для работы с БД
import os
from builtins import str
from typing import Dict, List

import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from models import Person, Base


class Repo(object):
    @staticmethod
    def validate_add_person(person) -> bool:
        return (person.id is None) and \
               (person.name is not None) and \
               (len(person.name.strip()) > 0)

    @staticmethod
    def validate_update_person(person_data: Dict[str, object]) -> bool:
        return 'id' in person_data

    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        # connStr = 'mysql+mysqlconnector://root:Ujvbhrf1557@localhost:3306/botdb'
        self.connStr = 'sqlite:///' + os.path.join(basedir, 'app.db')
        self.engine = create_engine(self.connStr, echo=False)
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

    def add_person(self, person) -> Dict[bool, Person]:
        if not Repo.validate_add_person(person):
            return {'ok': False, 'person': person}
        self.session.add(person)
        ok: bool = self.session_commit()
        return {'ok': ok, 'person': person}

    def add_persons(self, persons: List[Person]) -> List[Dict[bool, Person]]:
        results: List[Dict[bool, Person]] = list()
        for person in persons:
            result = self.add_person(person)
            results.append(result)
        return results

    def update_person(self, person_data: Dict[str, object]):
        if not Repo.validate_update_person(person_data):
            return {'ok': False, 'person': person_data}
        person = self.get_person(person_data['id'])

        for key in person_data:
            person.__dict__[key] = person_data[key]

        self.session.add(person)
        ok: bool = self.session_commit()
        return {'ok': ok, 'person': person}

    def update_persons(self, persons_data: List[Dict]):
        results: List[Dict[bool, Person]] = list()
        for person_data in persons_data:
            result = self.update_person(person_data)
            results.append(result)
        return results

    def get_person(self, person_id: int):
        person = self.session.query(Person).get(person_id)
        return person
