from pydantic import BaseModel, EmailStr


# 用于返回用户数据（可以选 id, name, email）
class UserOut(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True  # 支持从 ORM 对象读取数据（比如 User 实例）
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
