from sqlalchemy import *
from core.database import Base

class UserModels(Base):
    __tablename__='account'
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(255))
    email=Column(String(255))
    password=Column(String(255))
    avatar=Column(String(255))

class NoteModel(Base):
    __tablename__='note'
    id=Column(Integer,primary_key=True,autoincrement=True)
    author_id=Column(Integer,ForeignKey("account.id"))
    title=Column(String(255))
    content=Column(String(255))
    time=Column(DateTime)
    images=Column(JSON)
    likes=Column(Integer)
    favs=Column(Integer)

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

class JudgeModel(Base):
    __tablename__='judge'
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(50))
    description=Column(String(255))
    type=Column(String(50),ForeignKey("type1.typename"))
    star1=Column(Integer)
    star2=Column(Integer)
    star3=Column(Integer)
    star4=Column(Integer)
    star5=Column(Integer)

class JudgeCommentModel(Base):
    __tablename__='judgecomment'
    id=Column(Integer,autoincrement=True,primary_key=True)
    id_user = Column(Integer, ForeignKey("account.id"))
    id_judge = Column(Integer, ForeignKey("judge.id"))
    content=Column(String(255))
    time=Column(DateTime)

class TypeModel(Base):
    __tablename__="type1"
    typename=Column(String(255),primary_key=True)
    image=Column(String(255))

class FavJudgeModel(Base):
    __tablename__="favjudge"
    id_user=Column(Integer,ForeignKey("account.id"),primary_key=True)
    id_judge=Column(Integer,ForeignKey("judge.id"), primary_key=True)
    score=Column(Integer)
    time=Column(DateTime)
    islike=Column(Boolean)