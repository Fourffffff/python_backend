# main.py
from fastapi import FastAPI
from routers import User

app = FastAPI()

# 注册 user 路由，所有路径都以 /api 开头
app.include_router(User.router, prefix="/user", tags=["User"])
