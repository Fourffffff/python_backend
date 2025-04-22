from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.NoteSch import *
from schemas.OutSch import Response
from service import JudgeService

router=APIRouter()

@router.get("/get_all")
def get_all(type,db:Session=Depends(get_db)):
    print("get all: ",type)
    return JudgeService.get_all(type,db)

@router.get("/get_one")
def get_one(id,db:Session=Depends(get_db)):
    print("get one:",id)
    return JudgeService.get_one(id,db)

@router.get("/get_comments")
def get_comments(id,db:Session=Depends(get_db)):
    print("get comments: ",id)
    return JudgeService.get_comments(id,db)