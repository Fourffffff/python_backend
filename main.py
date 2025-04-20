# main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import UserRouters

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 允许所有来源（开发阶段可以写 *，生产建议具体写）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法，如 GET、POST 等
    allow_headers=["*"],  # 允许所有请求头
)
# 注册 user 路由，所有路径都以 /api 开头
app.include_router(UserRouters.router, prefix="/user", tags=["User"])
