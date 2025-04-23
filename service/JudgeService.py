from sqlalchemy.orm import Session
from models.Models import *
from schemas.JudgeSch import *
from schemas.OutSch import Response
import statistics


def get_all(type, db: Session):
    judges = db.query(JudgeModel).filter_by(type=type).all()
    res = []
    for i, judge in enumerate(judges):
        temp = JudgeSchema.from_orm(judge).dict()
        temp['score'] = sum(
            [temp['star1'] * 2, temp['star2'] * 4, temp['star3'] * 6, temp['star4'] * 8, temp['star5'] * 10])
        cnt = sum([temp['star1'], temp['star2'], temp['star3'], temp['star4'], temp['star5']])
        temp['score'] /= cnt
        res.append(temp)
    res.sort(key=lambda x: x['score'], reverse=True)
    for idx, item in enumerate(res, start=1):
        item['rank'] = idx
    return Response.success(res)


def get_one(id: int, db: Session):
    type = db.query(JudgeModel.type).filter_by(id=id).first()[0]
    judges = get_all(type, db)
    for judge in judges.data:
        if str(judge['id']) == str(id):
            judge['count']=sum([judge['star1'], judge['star2'],judge['star3'], judge['star4'], judge['star5']])
            return Response.success(judge)


def get_comments(id, db:Session):
    judgeComments=db.query(JudgeCommentModel).filter_by(id_judge=id).all()
    res=[]
    for judgeComment in judgeComments:
        temp=JudgeCommentSchema.from_orm(judgeComment).dict()
        temp['username']=db.query(UserModels.username).filter_by(id=temp['id_user']).first()[0]
        res.append(temp)
    print(res)
    return Response.success(res)


def get_types(db:Session):
    types=db.query(TypeModel).all()
    res=[]
    for type in types:
        res.append(JudgeTypeSche.from_orm(type).dict())
    return Response.success(res)