from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from core.database import get_db
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
def note_post(req:postRe,db:Session=Depends(get_db)):
    print("note_post: ",req)
    return NoteService.note_add(req,db)

@router.get("/get_all")
def note_get_all(id:int, db:Session=Depends(get_db)):
    print("get_all")
    return NoteService.get_all(id,db)

@router.get("/get_one")
def note_get_one(userId:int,noteId:int,db:Session=Depends(get_db)):
    print("get_one: ",userId," ",noteId)
    return NoteService.get_one(userId,noteId,db)

@router.post("/like")
def like(req:lfReq,db:Session=Depends(get_db)):
    print("like:",req.id_user,req.id_note)
    return NoteService.like(req,db)

@router.post("/fav")
def fav(req:lfReq,db:Session=Depends(get_db)):
    print("fav:",req.id_user,req.id_note)
    return NoteService.fav(req,db)

@router.post("/comment_post")
def comment_post(req:CommentReq,db:Session=Depends(get_db)):
    print(req)
    return NoteService.comment_post(req,db)