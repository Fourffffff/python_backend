import pytest
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.database import get_db
from models.Models import UserModels

@pytest.fixture(scope="session", autouse=True)
def init_db():
    # 这里自动在测试开始前运行
    db: Session = next(get_db())
    # 清空旧的数据（可选）
    # 添加初始用户
    user = UserModels(
        username="testuser",
        email="tests@example.com",
        password="testpassword"  # 这里是明文，如果你正式逻辑用加密，测试也要加密
    )
    db.add(user)
    db.commit()
    db.close()
