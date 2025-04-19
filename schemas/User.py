from pydantic import BaseModel
# 用于返回用户数据（可以选 id, name, email）
class UserOut(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True  # 支持从 ORM 对象读取数据（比如 User 实例）
