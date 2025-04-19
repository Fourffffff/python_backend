from sqlalchemy.orm import Session
from models.User import User

# 查询所有用户
def get_users(db: Session):
    return db.query(User).all()

