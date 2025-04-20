import random

from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.redis import r
from models.Models import UserModels
from schemas.UserSchemas import *
from schemas.OutSch import Response
from utils.emailUtils import send_email_code


def send_code(req: EmailRequest):
    code = str(random.randint(100000, 999999))
    r.set(req.email, code, ex=300)  # 设置过期时间为5分钟
    send_email_code(req.email, code)
    return {"msg": "验证码发送成功"}

def register(req,db: Session):
    real_code = r.get(req.email)
    if not real_code:
        raise HTTPException(status_code=400, detail="验证码已过期或无效")
    if req.code != real_code:
        raise HTTPException(status_code=400, detail="验证码错误")

    # 这里执行注册逻辑，如保存用户到数据库等
    r.delete(f"code:{req.email}")  # 用完就删除验证码
    user = UserModels(
        email=req.email,
        password=req.password,
        username="Null"
    )
    db.add(user)
    db.commit()
    return {"msg": "注册成功"}


def login(user:LoginRe, db:Session):
    if(db.query(UserModels).filter(UserModels.email==user.email,
                                   UserModels.password==user.password)):
        return Response().success()
    else:
        return "fail"
