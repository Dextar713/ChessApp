from . import db
from sqlalchemy import Column, ForeignKey, Integer, String
from flask_login import UserMixin


class User(db.Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), unique=True)
    name = Column(String(30), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)


db.create_tables()
