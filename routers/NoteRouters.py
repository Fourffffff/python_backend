from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from dependencis import get_current_user_id
from schemas.NoteSch import *
from schemas.OutSch import Response
import os
import uuid

from service import NoteService

router = APIRouter()

# 图片保存路径（确保这个路径存在或自动创建）
UPLOAD_DIR = "bucket/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_img")
async def upload_img(file: UploadFile = File(...)):
    try:
        # 获取原始扩展名
        suffix = os.path.splitext(file.filename)[-1]
        # 生成不重复文件名
        filename = f"{uuid.uuid4().hex}{suffix}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        # 写入文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 构建可访问图片的URL
        url=f"http://localhost:8000/images/{filename}"
        return Response.success(data=url)
    except Exception as e:
        return Response.fail(msg=str(e))
@router.post("/note_post")
def note_post(req:postRe,id= Depends(get_current_user_id),db:Session=Depends(get_db)):
    print("note_post: ",req)
    return NoteService.note_add(req,id,db)

@router.get("/get_all")
def note_get_all(id= Depends(get_current_user_id), db:Session=Depends(get_db)):
    print("get_all")
    return NoteService.get_all(id,db)

@router.get("/get_one")
def note_get_one(noteId:int,userId= Depends(get_current_user_id),db:Session=Depends(get_db)):
    print("get_one: ",userId," ",noteId)
    return NoteService.get_one(userId,noteId,db)

@router.post("/like")
def like(req:lfReq,user_id=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return NoteService.like(req,user_id,db)

@router.post("/fav")
def fav(req:lfReq,user_id=Depends(get_current_user_id), db:Session=Depends(get_db)):
    return NoteService.fav(req,user_id,db)

@router.post("/comment_post")
def comment_post(req:CommentReq,user_id=Depends(get_current_user_id), db:Session=Depends(get_db)):
    return NoteService.comment_post(req,user_id,db)