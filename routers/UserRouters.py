from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from core.database import get_db
from dependencis import get_current_user_id
from schemas.UserSchemas import *
import service.UserService as service

router = APIRouter()

@router.post("/send_code")
def send_code(req: EmailRequest):
    return service.send_code(req)

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return service.register(req,db)

@router.post("/login")
def login(user:LoginRe,db:Session=Depends(get_db)):
    print(f"login:{user}")
    return service.login(user,db)

@router.get("/get_avatar")
def get_avatar(id: int = Depends(get_current_user_id),db:Session=Depends(get_db)):
    return service.get_avatar(id,db)

@router.get("/get_username")
def get_username(id: str= Depends(get_current_user_id),db:Session=Depends(get_db)):
    print("get_username: ",id)
    return service.get_username(id,db)

@router.post("/avatar_update")
def avatar_update(avatarReq: AvatarReq,id:str= Depends(get_current_user_id),db:Session=Depends(get_db)):
    return service.avatar_update(avatarReq,id,db)

@router.post("/password_update")
def password_update(passwordReq:PasswordReq,id:str=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return service.password_update(passwordReq,id,db)