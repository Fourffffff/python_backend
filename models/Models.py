from sqlalchemy import *
from core.database import Base

class UserModels(Base):
    __tablename__='account'
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))

class NoteModel(Base):
    __tablename__='note'
    id=Column(Integer,primary_key=True,autoincrement=True)
    author_id=Column(Integer,ForeignKey("account.id"))
    title=Column(String(255))
    content=Column(String(255))
    time=Column(DateTime)
    likes=Column(Integer)
    favs=Column(Integer)
    images=Column(JSON)

class LikeModel(Base):
    __tablename__='like'
    id_user=Column(Integer, ForeignKey("account.id"),primary_key=True)
    id_note=Column(Integer, ForeignKey("note.id"), primary_key=True)
    time=Column(DateTime)

class FavModel(Base):
    __tablename__='fav'
    id_user=Column(Integer, ForeignKey("account.id"),primary_key=True)
    id_note=Column(Integer, ForeignKey("note.id"), primary_key=True)
    time=Column(DateTime)

class NoteCommentModel(Base):
    __tablename__='notecomment'
    id=Column(Integer,autoincrement=True,primary_key=True)
    id_user = Column(Integer, ForeignKey("account.id"))
    id_note = Column(Integer, ForeignKey("note.id"))
    content=Column(String(255))
    time=Column(DateTime)