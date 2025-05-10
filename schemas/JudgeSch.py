from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class JudgeSchema(BaseModel):
    id: int
    name:str
    description: str
    type: str
    star1:int
    star2:int
    star3:int
    star4:int
    star5:int
    rank: Optional[int] = 0  # ✅ 改为可选
    score: Optional[float] = 0 # ✅ 改为可选
    myscore:Optional[int]=0
    islike:Optional[bool]=False

    class Config:
        from_attributes = True

class JudgeCommentSchema(BaseModel):
    id: int
    id_user:int
    id_judge: int
    content: str
    time: datetime
    username:Optional[str]=None


    class Config:
        from_attributes = True  # 适配 SQLAlchemy ORM 模型（Pydantic v2 用法）

class JudgeTypeSche(BaseModel):
    typename:str
    image:str
    class Config:
        from_attributes=True

class RateReq(BaseModel):
    id_judge:int
    score:int

class LikeReq(BaseModel):
    id_judge:int

class CommentReq(BaseModel):
    id_judge:int
    content:str