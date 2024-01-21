import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
from turorial import app03,app04,app05,app06,app07
from fastapi.exceptions import HTTPException, RequestValidationError


# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
#请求地址：http://94.74.121.101:8000/  华为一年机器
#python -m pip install --upgrade pip
app = FastAPI(
    title='疫情跟踪器API文档',
    description='疫情跟踪器接口文档',
    version='1.0',
    docs_url='/docs',
    redoc_url='/redocs',
    # dependencies=[Depends(verify_token),Depends(verify_key)]

)
app.include_router(app03,prefix='/chapter03',tags=['第三章 请求参数和验证'])
app.include_router(app04,prefix='/chapter04',tags=['第四章 响应处理和fastAPI配置'])
app.include_router(app05,prefix='/chapter05',tags=['第五章 fastAPI依赖注入系统'])
app.include_router(app06,prefix='/chapter06',tags=['第六章 安全、认证和授权'])
app.include_router(app07,prefix='/chapter07',tags=['第七章 登录及系列接口'])
# uvicorn hello_world:app --reload

# @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request, exc:RequestValidationError):
# #     if 'regex' in str(exc):
# #         return JSONResponse({"code":"error",'message': str("密码不符合命名规则")})
# #     return JSONResponse({"code":"error",'message':str(exc)})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    if 'regex' in str(exc):
     return PlainTextResponse("{\"code\":\"error\",\"message\":\"密码不符合规则\"}", status_code=402)
    return PlainTextResponse(str(exc), status_code=402)


#mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static',app=StaticFiles(directory='./static'),name='static')

if __name__ == '__main__':

    uvicorn.run('run:app',host='0.0.0.1',port=8000,reload=True,debug=True,workers=1)