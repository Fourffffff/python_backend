# utils/response.py 或 schemas/ResponseSchemas.py

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class Response(GenericModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None  # 有些时候可以没有 data，比如错误信息

    @staticmethod
    def success(data: T = None, msg: str = "success") -> "Response":
        return Response(code=200, msg=msg, data=data)

    @staticmethod
    def fail(msg: str = "fail", code: int = 400) -> "Response":
        return Response(code=code, msg=msg, data=None)
