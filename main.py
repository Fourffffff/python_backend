# main.py
from fastapi import FastAPI
from routers import UserRouters

app = FastAPI()

# 注册 user 路由，所有路径都以 /api 开头
app.include_router(UserRouters.router, prefix="/user", tags=["User"])
