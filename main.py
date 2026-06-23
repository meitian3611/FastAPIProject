from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FastApi"}


"""
路径参数
路径参数的类型注解 - Path 自定义更多参数规则
"""


@app.get("/book/{ids}")
async def add(ids: Annotated[int, Path(ge=1, le=1000, description="图书id")]):
    return {"id": ids, "name": f"book name - {ids}"}


"""
查询参数
查询参数的类型注解 -  Query 自定义更多参数规则
字符串校验  - Annotated
"""


@app.get("/new/newList")
async def get_new_list(
        # page_index: int = Query(1, lt=100, description="页码，默认为1"),
        # page_size: int = Query(10,  description="每页数量，默认为10"),

        # 最新版本 - 推荐写法
        user_name: Annotated[str | None, Query(max_length=50, description="用户名")],
        page_index: Annotated[int, Query(ge=1, le=20, description="页码，默认为1")] = 1,
        page_size: Annotated[int, Query(ge=1, le=300, description="每页数量，默认为10")] = 10,
):
    return {"pageIndex": page_index, "pageSize": page_size, "userName": user_name}


"""
请求体参数
Field 自定义参数校验规则
Literal 枚举值
response_model 约束响应值格式
"""


class UserInfo(BaseModel):
    name: str = Field(max_length=50, min_length=1, description="用户名")
    age: int = Field(default=18, gt=0, lt=100, description="年龄")
    sex: str


@app.post("/userInfo", response_model=UserInfo)
async def get_user_info(user: UserInfo):
    return user


"""
错误异常处理
"""


@app.get("/error")
async def error():
    raise HTTPException(status_code=404, detail="用户不存在")


"""
中间件
执行顺序: 自底向上

中间件开始2
中间件开始1
中间件结束1
中间件结束2
"""


@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件开始1")
    response = await call_next(request)
    print("中间件结束1")
    return response


@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件开始2")
    response = await call_next(request)
    print("中间件结束2")
    return response


"""
依赖注入  Depends
"""


async def common_params(
        page_index: Annotated[int, Query(ge=1, le=20, description="页码，默认为1")] = 1,
        page_size: Annotated[int, Query(ge=1, le=300, description="每页数量，默认为10")] = 10,
):
    return {"pageIndex": page_index, "pageSize": page_size}


@app.get("/task/taskList")
async def get_task_list(params_info=Depends(common_params)): # 依赖注入
    return {
        "test": "1234",
        **params_info,
    }


