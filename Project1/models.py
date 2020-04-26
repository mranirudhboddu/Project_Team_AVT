import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class User(Base):

	#table creating
    __tablename__ = "users"
    username = Column(String, primary_key = True)
    password = Column(String, nullable = False)
    user_created_on = Column(DateTime, nullable = False)


    #data entry

    def __init__(self, username, password, user_created_on=None):
        self.username = username
        self.password = password
        self.user_created_on = datetime.now() 
 
    
