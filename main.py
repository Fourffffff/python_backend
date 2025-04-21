# main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import UserRouters, NoteRouters

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 允许所有来源（开发阶段可以写 *，生产建议具体写）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法，如 GET、POST 等
    allow_headers=["*"],  # 允许所有请求头
)
app.mount("/images", StaticFiles(directory="./bucket/images"), name="images")
app.include_router(UserRouters.router, prefix="/user", tags=["User"])
app.include_router(NoteRouters.router, prefix="/note", tags=["Notes"])