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


def get_one(judgeid: int,userid, db: Session):
    type = db.query(JudgeModel.type).filter_by(id=judgeid).first()[0]
    image=db.query(TypeModel.image).filter_by(typename=type).first()[0]
    judges = get_all(type, db)
    print(judges)
    judgeobj={}

    for judge in judges.data:
        if str(judge['id']) == str(judgeid):
            judge['count'] = sum([judge['star1'], judge['star2'], judge['star3'], judge['star4'], judge['star5']])
            judgeobj=judge
    temp=db.query(FavJudgeModel).filter_by(id_user=userid,id_judge=judgeid).first()
    judgeobj['image'] = image
    if temp:
        judgeobj['myscore']=temp.score
        judgeobj['islike']=temp.islike
    return Response.success(judgeobj)


def get_comments(id, db:Session):
    judgeComments=db.query(JudgeCommentModel).filter_by(id_judge=id).all()
    res=[]
    for judgeComment in judgeComments:
        temp=JudgeCommentSchema.from_orm(judgeComment).dict()
        temp['username']=db.query(UserModels.username).filter_by(id=temp['id_user']).first()[0]
        print("id and user",id,temp['id_user'])
        temp['score']=db.query(FavJudgeModel.score).filter_by(id_judge=id,id_user=temp['id_user']).first()[0]
        temp['avatarUrl']=db.query(UserModels.avatar).filter_by(id=temp['id_user']).first()[0]

        res.append(temp)
    print(res)
    return Response.success(res)


def get_types(db:Session):
    types=db.query(TypeModel).all()
    res=[]
    for type in types:
        res.append(JudgeTypeSche.from_orm(type).dict())
    return Response.success(res)


def rate(req:RateReq,id_user, db:Session):
    rateobj=db.query(FavJudgeModel).filter_by(id_user=id_user,id_judge=req.id_judge).first()
    judgeobj = db.query(JudgeModel).filter_by(id=req.id_judge).first()

    if rateobj:
        rate=rateobj.score
        if rate == 1:
            judgeobj.star1 -= 1
        elif rate == 2:
            judgeobj.star2 -= 1
        elif rate == 3:
            judgeobj.star3 -= 1
        elif rate == 4:
            judgeobj.star4 -= 1
        elif rate == 5:
            judgeobj.star5 -= 1

        rateobj.score=req.score

        if req.score == 1:
            judgeobj.star1 += 1
        elif req.score == 2:
            judgeobj.star2 += 1
        elif req.score == 3:
            judgeobj.star3 += 1
        elif req.score == 4:
            judgeobj.star4 += 1
        elif req.score == 5:
            judgeobj.star5 += 1

        db.commit()
    else:
        model= FavJudgeModel(**req.dict(),id_user=id_user  ,time=datetime.now(),islike=0)
        if req.score == 1:
            judgeobj.star1 += 1
        elif req.score == 2:
            judgeobj.star2 += 1
        elif req.score == 3:
            judgeobj.star3 += 1
        elif req.score == 4:
            judgeobj.star4 += 1
        elif req.score == 5:
            judgeobj.star5 += 1
        db.add(model)
        db.commit()
    return Response.success()


def like(req,id_user, db:Session):
    rateobj = db.query(FavJudgeModel).filter_by(id_user=id_user, id_judge=req.id_judge).first()
    if rateobj:
        rateobj.islike = 1-rateobj.islike
        db.commit()
    else:
        model = FavJudgeModel(**req.dict(), id_user=id_user,time=datetime.now(), islike=1,score=0)
        db.add(model)
        db.commit()
    return Response.success()


def comment_post(req:CommentReq,id_user, db:Session):
    rateobj = db.query(FavJudgeModel).filter_by(id_user=id_user, id_judge=req.id_judge).first()
    if rateobj:
        model=JudgeCommentModel(
            **req.dict(),
            id_user=id_user,
            time=datetime.now()
        )
        db.add(model)
        db.commit()
        return Response.success()
    else:
        return Response.fail("未评分不能评论")