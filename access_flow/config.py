import os

class Config:
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "database.db")