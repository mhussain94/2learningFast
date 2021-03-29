from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


#Model for blog class for DB
#Creating tables
class Blog(Base):
    __tablename__ = 'blogs' #defining table name

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    body = Column(String, index=True)

class User(Base):
    __tablename__ = 'users' #defining table name

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)

