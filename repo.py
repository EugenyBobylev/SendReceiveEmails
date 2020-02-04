# репозиторий для работы с БД
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Repo(object):
    def __init__(self):
        connStr = 'mysql+mysqlconnector://root:Ujvbhrf1557@localhost:3306/botdb'
        engine = create_engine(connStr, echo=False)
        Base = declarative_base()
        Base.metadata.create_all(engine, checkfirst=True)
        self.session = self.CreateSession(engine)

