import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MyDB:
    DB_URI = "mysql+mysqlconnector://root:abcd7777@localhost:3306/giraffe"

    def __init__(self):
        self.Base = sqlalchemy.orm.declarative_base()
        self.engine = create_engine(MyDB.DB_URI)
        self.create_tables()
        self.session = sessionmaker(bind=self.engine)()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)


db = MyDB()
