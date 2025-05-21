import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from models.Models import NoteModel
from routers import NoteRouters
from dependencis import get_current_user_id  # 正确引用依赖函数

client = TestClient(app)

# 创建 mock db 并替代 get_db
mock_db = MagicMock()

def override_get_db():
    yield mock_db

def override_get_current_user_id():
    return 1

# 依赖覆盖
app.dependency_overrides[NoteRouters.get_db] = override_get_db
app.dependency_overrides[get_current_user_id] = override_get_current_user_id

# 上传图片测试
def test_upload_img():
    with open("test_image.png", "rb") as f:
        response = client.post("/note/upload_img", files={"file": ("test_image.jpg", f, "image/jpeg")})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert "http://localhost:8000/images/" in response.json()["data"]

# 发布笔记
def test_note_post(monkeypatch):
    mock_add = MagicMock(return_value={"code": 200, "msg": "success", "data": None})
    monkeypatch.setattr("service.NoteService.note_add", mock_add)

    payload = {
        "title": "Test Note",
        "content": "This is a test note.",
        "images": []
    }
    response = client.post("/note/note_post", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200
    mock_add.assert_called_once()

# 获取所有笔记
def test_get_all(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": []}
    monkeypatch.setattr("service.NoteService.get_all", lambda id, db: mock_response)
    response = client.get("/note/get_all")
    assert response.status_code == 200
    assert response.json()["code"] == 200

# 获取某一条笔记
def test_get_one(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": {"note": {}, "isliked": False, "isfav": False, "comments": []}}
    monkeypatch.setattr("service.NoteService.get_one", lambda userId, noteId, db: mock_response)
    response = client.get("/note/get_one", params={"noteId": 1})
    assert response.status_code == 200
    assert response.json()["code"] == 200

# 点赞接口测试
def test_like(monkeypatch):
    monkeypatch.setattr("service.NoteService.like", lambda req, user_id, db: {"code": 200, "msg": "like", "data": None})
    response = client.post("/note/like", json={"id_note": 1})
    assert response.status_code == 200
    assert response.json()["msg"] in ["like", "unlike"]

# 收藏接口测试
def test_fav(monkeypatch):
    monkeypatch.setattr("service.NoteService.fav", lambda req, user_id, db: {"code": 200, "msg": "fav", "data": None})
    response = client.post("/note/fav", json={"id_note": 1})
    assert response.status_code == 200
    assert response.json()["msg"] in ["fav", "unfav"]

# 评论发布
def test_comment_post(monkeypatch):
    monkeypatch.setattr("service.NoteService.comment_post", lambda req, user_id, db: {"code": 200, "msg": "success", "data": None})
    response = client.post("/note/comment_post", json={
        "id_note": 1,
        "content": "This is a comment"
    })
    assert response.status_code == 200
    assert response.json()["code"] == 200

# 获取收藏夹
def test_get_collection(monkeypatch):
    monkeypatch.setattr("service.NoteService.get_collection", lambda user_id, db: {"code": 200, "msg": "success", "data": []})
    response = client.get("/note/get_collection")
    assert response.status_code == 200
    assert response.json()["code"] == 200

# 获取我的笔记
def test_get_mynotes(monkeypatch):
    monkeypatch.setattr("service.NoteService.get_mynotes", lambda user_id, db: {"code": 200, "msg": "success", "data": []})
    response = client.get("/note/get_mynotes")
    assert response.status_code == 200
    assert response.json()["code"] == 200
