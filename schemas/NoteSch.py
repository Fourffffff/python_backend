from typing import List
from datetime import time, datetime

from pydantic import BaseModel
from typing import Optional


class postRe(BaseModel):
    title:str
    content:str
    id:int
    images:List[str]

class NotesResponse(BaseModel):
    id: int
    author_name: str
    title: str
    content: str
    time: datetime
    likes:Optional[int]=0
    favs: Optional[int]=0
    images: list

    class Config:
        from_attributes = True

class lfReq(BaseModel):
    id_user:int
    id_note:int

class CommentReq(BaseModel):
    id_note:int
    id_user:int
    content:str