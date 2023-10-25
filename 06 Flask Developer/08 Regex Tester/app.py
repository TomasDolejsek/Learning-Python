from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask
from os.path import exists
import sys


app = Flask(__name__)
Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'

    regex = Column(String(50))
    text = Column(String(1024))
    result = Column(Boolean)

class DatabaseProcessor():
    def __init__(self):
        DATABASE_NAME = 'db.sqlite3'
        engine = create_engine("sqlite:///" + DATABASE_NAME, echo=False)
        self.session = sessionmaker(bind=engine)()
        if not exists(DATABASE_NAME):
            Base.metadata.create_all(engine)



# don't change the following way to run flask:
if __name__ == '__main__':
    db = DatabaseProcessor()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
