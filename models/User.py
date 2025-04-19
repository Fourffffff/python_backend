from sqlalchemy import Column,Integer,String
from database import Base

class User(Base):
    __tablename__='test'
    name=Column(String(255),primary_key=True)
    age=Column(Integer,primary_key=True)
