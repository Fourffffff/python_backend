from typing import List
from datetime import time, datetime

from fastapi import Depends
from pydantic import BaseModel
from typing import Optional

from dependencis import get_current_user_id


class postRe(BaseModel):
    title:str
    content:str
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
    id_note:int

class CommentReq(BaseModel):
    id_note:int
    content:str

