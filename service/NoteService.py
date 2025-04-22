from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.Models import *
from schemas.NoteSch import *
from schemas.OutSch import Response


def note_add(req:postRe, db:Session):
    new_note = NoteModel(
        author_id=req.id,
        title=req.title,
        content=req.content,
        time=datetime.now().time(),  # 或 datetime.now() 如果你用 DateTime 类型
        likes=0,
        favs=0,
        images=req.images
    )
    db.add(new_note)
    db.commit()
    return Response.success()


def get_all(id,db:Session):
    # 手动进行 JOIN 查询来获取 Note 和 UserModels 数据
    notes = db.query(
        NoteModel,
        UserModels.username # 获取关联的用户名
    ).join(UserModels, NoteModel.author_id == UserModels.id).all()

    # 返回时，提取用户名并构建结果
    return Response.success([{
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "time": note.time,
        "likes": note.likes,
        "favs": note.favs,
        "images": note.images,
        "username":username,  # 使用查询结果中的用户名
        "isliked":db.query(LikeModel).filter_by(id_user=id, id_note=note.id).first() is not None,
        "isfav":db.query(FavModel).filter_by(id_user=id, id_note=note.id).first() is not None,
    } for note,username in notes])


def get_one(userId, noteId, db:Session):
    note=db.query(NoteModel).filter_by(id=noteId).first()
    isliked=db.query(LikeModel).filter_by(id_user=userId, id_note=note.id).first() is not None
    isfav=db.query(FavModel).filter_by(id_user=userId, id_note=note.id).first() is not None
    comments=db.query(NoteCommentModel).filter_by(id_note=noteId).all()
    comments_list = [
        {
            "id": comment.id,
            "username": db.query(UserModels).filter_by(id=comment.id_user).first().username,
            "id_note": comment.id_note,
            "content":comment.content,
            "time": comment.time
        }
        for comment in comments
    ]
    return Response.success(
        {
            "note": {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "time": note.time,
                "author_id": note.author_id,
                "images":note.images
            },
            "isliked": isliked,
            "isfav": isfav,
            "comments": comments_list  # 这里是已经转换为字典的评论数据
        }
    )
