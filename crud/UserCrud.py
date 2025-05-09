from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.redis import r
from models.Models import UserModels
from routers.NoteRouters import UPLOAD_DIR
from schemas.UserSchemas import *
from schemas.OutSch import Response
from utils.emailUtils import send_email_code

def get_user_byemail(user:LoginRe,db:Session):
    return (db.query(UserModels).filter(UserModels.email == user.email)).first()

def get_avatar(id, db:Session):
    return db.query(UserModels).filter_by(id=id).first().avatar

def get_username(id,db:Session):
    return db.query(UserModels).filter_by(id=id).first().username