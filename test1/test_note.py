from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

def test_get_all_notes():
    response = client.get("/note/get_all", params={"id": 1})
    assert response.status_code == 200
    print(response.json())

def test_get_one_note():
    response = client.get("/note/get_one", params={"userId": 1, "noteId": 1})
    assert response.status_code == 200
    print(response.json())

def test_like_note():
    response = client.post("/note/like", json={"id_user": 1, "id_note": 1})
    assert response.status_code == 200
    print(response.json())

def test_fav_note():
    response = client.post("/note/fav", json={"id_user": 1, "id_note": 1})
    assert response.status_code == 200
    print(response.json())

def test_comment_note():
    response = client.post("/note/comment_post", json={
        "id_user": 1,
        "id_note": 1,
        "content": "pytest 自动化测试评论"
    })
    assert response.status_code == 200
    print(response.json())
