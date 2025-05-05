# test_main.py 或 test_your_router.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # 注意替换为你实际的 FastAPI 应用
from schemas.OutSch import Response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# 如果你是从 APIRouter 注册到 app 的，请确保 app 是完整注册后的

client = TestClient(app)

@patch("service.UserService.get_username")  # 路径要改成你实际代码中 service 的导入路径
def test_get_username(mock_get_username):
    # 设置 mock 返回值
    mock_get_username.return_value = Response.success("Tom")

    # 发起请求
    response = client.get("/user/get_username?id=1")
    print(response)

    # 断言状态码是否为 200
    assert response.status_code == 200

    # 断言返回的内容是否正确
    assert response.json() == {'code': 200, 'data': 'Tom', 'msg': 'success'}

    # 断言 mock 的函数是否被正确调用
    # 第二个参数是 db，但因为被 FastAPI 注入，这里我们只检查 id 是否传了正确
    mock_get_username.assert_called_once()
    called_args = mock_get_username.call_args[0]  # 获取位置参数
    assert called_args[0] == 1  # 第一个参数是 id
