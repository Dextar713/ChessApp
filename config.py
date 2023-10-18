import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:abcd7777@localhost:3306/giraffe'
SQLALCHEMY_TRACK_MODIFICATIONS = False
