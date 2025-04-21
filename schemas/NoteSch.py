from typing import List
from datetime import time, datetime

from pydantic import BaseModel


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
    likes: int
    favs: int
    images: list

    class Config:
        from_attributes = True
