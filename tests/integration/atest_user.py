from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app


client = TestClient(app)

# def test_send_code():
#     response = client.post("/user/send_code", json={"email": "tests@example.com"})
#     assert response.status_code == 200
#     print(response.json())
# without redis

# def test_register():
#     response = client.post("/user/register", json={
#         "username": "testuser",
#         "email": "tests@example.com",
#         "password": "123456",
#         "code": "1234"   # 测试时可以假设是 1234
#     })
#     assert response.status_code == 200
#     print(response.json())

def test_login():
    response = client.post("/user/login", json={
        "email": "tests@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    print(response.json())
