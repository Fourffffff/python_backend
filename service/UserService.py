import os
import random
from utils.securityUtils import hash_password, verify_password
from utils.verifyUtils import *
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.redis import r
from models.Models import UserModels
from routers.NoteRouters import UPLOAD_DIR
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
        password=hash_password(req.password),
        username="Null"
    )
    db.add(user)
    db.commit()
    return {"msg": "注册成功"}


def login(user:LoginRe, db:Session):
    user1=(db.query(UserModels).filter(UserModels.email == user.email)).first()
    print("user1",user1)
    print(user1.password)
    if verify_password(user.password, user1.password):
        token = create_access_token({"sub": str(user1.id)}, timedelta(minutes=60))
        print("token", token)
        return Response().success(token)
    else:
        if not (db.query(UserModels).filter(UserModels.email == user.email)).first():
            return Response().fail("该邮箱未注册")


        else:
            return Response().fail("密码错误")


def get_avatar(id, db:Session):
    avatar=db.query(UserModels).filter_by(id=id).first().avatar
    return Response.success(avatar)

def get_username(id,db:Session):
    username=db.query(UserModels).filter_by(id=id).first().username
    return Response.success(username)


def avatar_update(avatarReq,id, db:Session):
    user=db.query(UserModels).filter_by(id=id).first()
    # 删除旧头像（如果不是默认头像）
    if user.avatar and "localhost:8000/images/" in user.avatar:
        old_filename = user.avatar.split("/")[-1]
        old_path = os.path.join(UPLOAD_DIR, old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)
    user.avatar=avatarReq.avatarUrl

    db.commit()
    return Response.success()


def password_update(passwordReq, id, db:Session):
    user=db.query(UserModels).filter_by(id=id).first()
    if not verify_password(passwordReq.old, user.password):
        return Response.fail("旧密码错误")
    elif passwordReq.password!=passwordReq.password1:
        print("password:",passwordReq.password,' ',passwordReq.password1)
        return Response.fail("两次输入密码不一致")
    else:
        user.password=hash_password(passwordReq.password)
        db.commit()
        return Response.success()