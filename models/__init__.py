import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI


class MyDB:
    DB_URI = SQLALCHEMY_DATABASE_URI

    def __init__(self):
        self.Base = sqlalchemy.orm.declarative_base()
        self.engine = create_engine(MyDB.DB_URI)
        self.create_tables()
        self.session = sessionmaker(bind=self.engine)()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)


db = MyDB()
