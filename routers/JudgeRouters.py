from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.JudgeSch import RateReq, LikeReq
from schemas.NoteSch import *
from schemas.OutSch import Response
from service import JudgeService

router=APIRouter()

@router.get("/get_all")
def get_all(type,db:Session=Depends(get_db)):
    print("get all: ",type)
    return JudgeService.get_all(type,db)

@router.get("/get_one")
def get_one(judgeid,userid,db:Session=Depends(get_db)):
    print("get one:",judgeid,' ',userid)
    return JudgeService.get_one(judgeid,userid,db)

@router.get("/get_comments")
def get_comments(id,db:Session=Depends(get_db)):
    print("get comments: ",id)
    return JudgeService.get_comments(id,db)

@router.get("/get_types")
def get_types(db:Session=Depends(get_db)):
    return JudgeService.get_types(db)

@router.post("/rate")
def rate(req:RateReq,db:Session=Depends(get_db)):
    return JudgeService.rate(req,db)

@router.post("/likechange")
def like(req:LikeReq,db:Session=Depends(get_db)):
    return JudgeService.like(req,db)

@router.post("/comment_post")
def comment_post(req:CommentReq,db:Session=Depends(get_db)):
    return JudgeService.comment_post(req,db)