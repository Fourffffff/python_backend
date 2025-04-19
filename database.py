from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 替换成你自己的 MySQL 信息（确保数据库已创建）
DATABASE_URL = "mysql+pymysql://root:123123@localhost:3306/my_shangxiao_db?charset=utf8mb4"

# 创建数据库引擎（负责连接）
engine = create_engine(DATABASE_URL, echo=True)

# 创建数据库会话类（操作数据库用）
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 创建模型基类（所有模型都从这里继承）
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()