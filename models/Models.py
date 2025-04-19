from sqlalchemy import Column,Integer,String
from core.database import Base

class UserModels(Base):
    __tablename__='account'
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))
