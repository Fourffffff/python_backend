import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from models.Models import UserModels
from routers import UserRouters
from dependencis import get_current_user_id  # 正确引用依赖函数

client = TestClient(app)

# 创建 mock db 并替代 get_db
mock_db = MagicMock()

def override_get_db():
    yield mock_db

def override_get_current_user_id():
    return 1

# 依赖覆盖
app.dependency_overrides[UserRouters.get_db] = override_get_db
app.dependency_overrides[get_current_user_id] = override_get_current_user_id

# 测试发送验证码
@patch("service.UserService.r.set")
@patch("service.UserService.send_email_code")
def test_send_code(mock_send_email, mock_redis_set):
    response = client.post("/user/send_code", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["msg"] == "验证码发送成功"
    mock_redis_set.assert_called_once()
    mock_send_email.assert_called_once()

# 测试注册

# 测试登录成功
@patch("service.UserService.verify_password", return_value=True)
@patch("service.UserService.create_access_token", return_value="testtoken")
def test_login_success(mock_token, mock_verify):
    user = UserModels(id=1, email="test@example.com", password="hashed_password")
    mock_db.query().filter().first.return_value = user

    response = client.post("/user/login", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert response.json()["data"] == "testtoken"

# 测试获取头像
def test_get_avatar():
    mock_user = UserModels(id=1, avatar="http://localhost:8000/images/avatar.jpg")
    mock_db.query().filter_by().first.return_value = mock_user

    response = client.get("/user/get_avatar")
    assert response.status_code == 200
    assert response.json()["data"] == mock_user.avatar

# 测试获取用户名
def test_get_username():
    mock_user = UserModels(id=1, username="tester")
    mock_db.query().filter_by().first.return_value = mock_user

    response = client.get("/user/get_username")
    assert response.status_code == 200
    assert response.json()["data"] == mock_user.username

# 测试头像更新
@patch("os.path.exists", return_value=True)
@patch("os.remove")
def test_avatar_update(mock_remove, mock_exists):
    user = UserModels(id=1, avatar="http://localhost:8000/images/old.png")
    mock_db.query().filter_by().first.return_value = user

    response = client.post("/user/avatar_update", json={
        "avatarUrl": "http://localhost:8000/images/new.png"
    })
    assert response.status_code == 200
    assert response.json()["code"] == 200
    mock_remove.assert_called_once()
    assert user.avatar == "http://localhost:8000/images/new.png"
