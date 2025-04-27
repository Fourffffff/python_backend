from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app


client = TestClient(app)

def test_get_all_judges():
    response = client.get("/judge/get_all", params={"type": "电子产品"})
    assert response.status_code == 200
    print(response.json())

def test_get_one_judge():
    response = client.get("/judge/get_one", params={"judgeid": 1, "userid": 1})
    assert response.status_code == 200
    print(response.json())

def test_get_comments_judge():
    response = client.get("/judge/get_comments", params={"id": 1})
    assert response.status_code == 200
    print(response.json())

def test_get_types():
    response = client.get("/judge/get_types")
    assert response.status_code == 200
    print(response.json())

def test_rate_judge():
    response = client.post("/judge/rate", json={
        "id_user": 1,
        "id_judge": 1,
        "score": 5
    })
    assert response.status_code == 200
    print(response.json())

def test_likechange_judge():
    response = client.post("/judge/likechange", json={
        "id_user": 1,
        "id_judge": 1
    })
    assert response.status_code == 200
    print(response.json())

def test_comment_post_judge():
    response = client.post("/judge/comment_post", json={
        "id_user": 1,
        "id_judge": 1,
        "content": "pytest自动化测试评论-judge"
    })
    assert response.status_code == 200
    print(response.json())
