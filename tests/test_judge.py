import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from routers import JudgeRouters
from dependencis import get_current_user_id

client = TestClient(app)

# 替代依赖项
mock_db = MagicMock()

def override_get_db():
    yield mock_db

def override_get_current_user_id():
    return 1

app.dependency_overrides[JudgeRouters.get_db] = override_get_db
app.dependency_overrides[get_current_user_id] = override_get_current_user_id

# GET /judge/get_all
def test_get_all(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": []}
    monkeypatch.setattr("service.JudgeService.get_all", lambda type, db: mock_response)
    response = client.get("/judge/get_all", params={"type": "test"})
    assert response.status_code == 200
    assert response.json()["code"] == 200

# GET /judge/get_one
def test_get_one(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": {"id": 1, "myscore": 5, "islike": 1}}
    monkeypatch.setattr("service.JudgeService.get_one", lambda judgeid, userid, db: mock_response)
    response = client.get("/judge/get_one", params={"judgeid": 1})
    assert response.status_code == 200
    assert response.json()["code"] == 200

# GET /judge/get_comments
def test_get_comments(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": []}
    monkeypatch.setattr("service.JudgeService.get_comments", lambda id, db: mock_response)
    response = client.get("/judge/get_comments", params={"id": 1})
    assert response.status_code == 200
    assert response.json()["code"] == 200

# GET /judge/get_types
def test_get_types(monkeypatch):
    mock_response = {"code": 200, "msg": "success", "data": ["A", "B", "C"]}
    monkeypatch.setattr("service.JudgeService.get_types", lambda db: mock_response)
    response = client.get("/judge/get_types")
    assert response.status_code == 200
    assert response.json()["code"] == 200

# POST /judge/rate
def test_rate(monkeypatch):
    monkeypatch.setattr("service.JudgeService.rate", lambda req, id_user, db: {"code": 200, "msg": "success", "data": None})
    payload = {
        "id_judge": 1,
        "score": 5
    }
    response = client.post("/judge/rate", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200

# POST /judge/likechange
def test_likechange(monkeypatch):
    monkeypatch.setattr("service.JudgeService.like", lambda req, id_user, db: {"code": 200, "msg": "success", "data": None})
    payload = {
        "id_judge": 1
    }
    response = client.post("/judge/likechange", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200

# POST /judge/comment_post
def test_comment_post(monkeypatch):
    monkeypatch.setattr("service.JudgeService.comment_post", lambda req, id_user, db: {"code": 200, "msg": "success", "data": None})
    payload = {
        "id_judge": 1,
        "content": "This is a test comment."
    }
    response = client.post("/judge/comment_post", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200
