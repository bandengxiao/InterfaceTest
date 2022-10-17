from fastapi import FastAPI,APIRouter,Depends,Header,HTTPException
from typing import Optional

#依赖注入系统
#依赖注入系统是指在编程中，为保证代码成功运行，先导入或声明其所需要的“依赖”，如子函数、数据库连接等
#提高代码的复用率、共享数据库连接、增强安全、认证、角色管理

'''
FastApi的兼容性
支持所有的关系型数据库，支撑NoSQL数据库
兼容第三方的包和API
认证和授权系统
响应数据注入系统
'''
app05 = APIRouter ()

#创建导入和声明依赖

def common_param(q:Optional[str]=None,page:int=1,limit:int=100):
    return {"q":q,"page":page,"limit":limit}

@app05.get("/dependency_01")
def dependency01(commons:dict=Depends(common_param)):
    return commons

@app05.get("/dependency_02")
async def dependency02(commons:dict=Depends(common_param)):
    return commons

#类作为依赖项
fake_item_db=[{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]
class CommonQueryParams:
    def __init__(self,q:Optional[str]=None,page:int=1,limit:int=100):
        self.q=q
        self.page=page
        self.limit=limit
@app05.get("/class_as_dependencies")
def classes_as_dependencies(commons:CommonQueryParams=Depends(CommonQueryParams)):
# def classes_as_dependencies(commons: CommonQueryParams = Depends()): 三种写法，作用一样
# def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    return commons

# 路径操作装饰器中的多依赖
def verify_key(x_key:str=Header(...)):
    #有返回值的子依赖，但是返回值不会被调用
    if x_key != "fake-x_key":
      raise HTTPException(status_code=400,detail="fake")
    return x_key

def verify_token(x_token:str=Header(...)):
    #有返回值的子依赖，但是返回值不会被调用
    if x_token != "fake-x_token":
      raise HTTPException(status_code=400,detail="fake")
    return x_token


@app05.get("dependency_in_path_operation",dependencies=[Depends(verify_token),Depends(verify_key)])
def dependency_in_path_operation():
    return [{"user":"user01"},{"user":"user02"}]

#全局依赖
# app05=APIRouter(dependencies=[Depends(verify_token),Depends(verify_key)])

#带yeild的依赖 需要Python3.7版本才支持，Python3.6需要pip install async-exit-stack async-generator
async def get_db():
    db="db_conn"
    try:
        yield db
    finally:
        db.endswith("close")
