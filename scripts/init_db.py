from core.database import engine, SessionLocal
from models.Models import Base, UserModels, NoteModel, LikeModel, FavModel, NoteCommentModel, JudgeModel, JudgeCommentModel, TypeModel, FavJudgeModel
from sqlalchemy.orm import Session
from datetime import datetime

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)

    # 填充一些初始数据
    db = Session(bind=engine)

    try:
        # 添加一个测试用户
        user = UserModels(username="testuser", email="test1@example.com", password="123456")
        db.add(user)
        db.commit()
        db.refresh(user)

        # 添加一个分类
        type1 = TypeModel(typename="电子产品", image="image_url")
        db.add(type1)
        db.commit()

        # 添加一个judge
        judge = JudgeModel(
            name="iPhone 15",
            description="Apple 新手机",
            type=type1.typename,
            star1=1,
            star2=2,
            star3=3,
            star4=4,
            star5=5
        )
        db.add(judge)
        db.commit()
        db.refresh(judge)

        # 添加一篇笔记
        note = NoteModel(
            author_id=user.id,
            title="我的第一篇笔记",
            content="这是一条测试内容",
            time=datetime.now(),
            images=[],
            likes=0,
            favs=0
        )
        db.add(note)
        db.commit()
        db.refresh(note)

        # 添加评论
        comment = NoteCommentModel(
            id_user=user.id,
            id_note=note.id,
            content="很棒的笔记！",
            time=datetime.now()
        )
        db.add(comment)
        db.commit()

        # 添加收藏
        fav = FavModel(
            id_user=user.id,
            id_note=note.id,
            time=datetime.now()
        )
        db.add(fav)
        db.commit()

        # 添加点赞
        like = LikeModel(
            id_user=user.id,
            id_note=note.id,
            time=datetime.now()
        )
        db.add(like)
        db.commit()

        # 添加评分收藏
        fav_judge = FavJudgeModel(
            id_user=user.id,
            id_judge=judge.id,
            score=5,
            time=datetime.now(),
            islike=True
        )
        db.add(fav_judge)
        db.commit()

        # 添加评分评论
        judge_comment = JudgeCommentModel(
            id_user=user.id,
            id_judge=judge.id,
            content="非常棒的产品！",
            time=datetime.now()
        )
        db.add(judge_comment)
        db.commit()

        print("数据库初始化完成！")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
