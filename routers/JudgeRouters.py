from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from dependencis import get_current_user_id
from schemas.JudgeSch import *
from schemas.OutSch import Response
from service import JudgeService

router=APIRouter()

@router.get("/get_all")
def get_all(type,db:Session=Depends(get_db)):
    print("get all: ",type)
    return JudgeService.get_all(type,db)

@router.get("/get_one")
def get_one(judgeid,userid= Depends(get_current_user_id),db:Session=Depends(get_db)):
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
def rate(req:RateReq,id_user=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return JudgeService.rate(req,id_user,db)

@router.post("/likechange")
def like(req:LikeReq,id_user=Depends(get_current_user_id), db:Session=Depends(get_db)):
    return JudgeService.like(req,id_user, db)

@router.post("/comment_post")
def comment_post(req:CommentReq,id_user=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return JudgeService.comment_post(req,id_user,db)