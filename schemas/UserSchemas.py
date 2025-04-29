from pydantic import BaseModel, EmailStr


# 用于返回用户数据（可以选 id, name, email）
class UserOut(BaseModel):
    name: str
    age: int
# 请求验证码模型
class EmailRequest(BaseModel):
    email: EmailStr

# 注册请求模型
class RegisterRequest(BaseModel):
    email: EmailStr
    code: str
    password: str

class LoginRe(BaseModel):
    email:EmailStr
    password:str

class AvatarReq(BaseModel):
    id:int
    avatar:str