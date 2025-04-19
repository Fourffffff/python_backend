from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from core.database import get_db
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

