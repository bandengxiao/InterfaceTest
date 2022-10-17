from fastapi import APIRouter , status ,Form,File,UploadFile,HTTPException
from pydantic import BaseModel,EmailStr
from typing import Optional,List,Union

app04 = APIRouter ()

# response Model 响应模型
class UserIn(BaseModel):
    userName:str
    pwd:str
    Email:EmailStr
    mobile:str="10086"
    address:str=None
    full_Name:str=None



class UserOut(BaseModel):
    userName: str
    Email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_Name: str = None

users={
    "user01":{"userName":"user01","Email":"924106952@qq.com","address":"北京市","full_Name":"测试用户","mobile":"10086"},
    "user02":{"userName":"user02","Email":"924106952@qq.com","mobile":"13022558896","address":"北京市","full_Name":"测试用户","mobile":"10086"}
}


@app04.post('/response_Model',response_model=UserOut,response_model_exclude_unset=True)
async def response_model(userIn:UserIn):
    print(userIn.userName)
    return users["user01"]

@app04.post('/response_model/attribute',
            # response_model=UserOut
            # response_model_include=["userName","Email"] 列出需要在返回结果中包含的字段
            # response_model_exclude=["userName"] 列出需要在返回结果中去除的字段
            # response_model=Union[UserIn,UserOut]
            response_model=List[UserOut] #与列表中的模型类相匹配则返回对应模型类数据格式
            )
async def response_model_attributes(user:UserIn):

    return user


#响应状态码
@app04.post('/status_code',status_code=status.HTTP_200_OK)
async def status_code():
    return {"status_code":200}

# 表单数据处理
@app04.post('/login')
async def login(user:str = Form(...),password:str=Form(...)): #定义表单参数  Form类的元数据和校验方法类似Body、Query、Path、Cookie
    return {"user":user}
#单文件、多文件上传及参数详解

@app04.post('/file')##上传单个文件，仅适合上传小文件
async def file(file:bytes=File(...)):
    return {"file_size":len(file)}


@app04.post('/files')#上传多个文件
async def file(files:List[bytes]=File(...)):
    return {"file_size":"多个文件"}



@app04.post('/bigFile')
async def upload_files(files:List[UploadFile]=File(...)):
    '''
    使用uploadFile类的优势
    1、文件存储在内存当中，使用内存达到阈值后，将被保存在磁盘中
    2、适合大文件、视频上传
    3、可以获取上传的文件的元数据、如文件名、创建时间等
    4、有文件对象的异步接口
    5、上传的文件是python的文件对象，如write(),read(),seek(),close()操作
    :param files:
    :return:
    '''

    for file in files:
        content=await file.read()
        print(content)
    return {"file_name":files[0].filename,"content_type":files[0].content_type}


#【见run.py】FastApi项目的静态文件的配置

#Path Operation Configuration 路径操作配置

@app04.post(
    "/path_operation_configuration",
    response_model=UserOut,
    # tags=["path","operation","Configuration"],
    summary="This is summary",
    description="This is description",
    response_description="this is response_description",
    deprecated=True,
    status_code=status.HTTP_200_OK
)
async def path_operation(user:UserIn):
    return {"code":"200"}



#应用常见的配置项 【见run.py】

# 错误处理
@app04.get('/http_exception')
def http_exception(city:str):
    if city != 'beijing ':
        raise HTTPException(status_code=404,detail='city not found',headers={"Error_code":"ERROR"})
    return {"city":city}


@app04.get('/http_exception/{city_id}')
def override_http_exception(city_id:int):
    if city_id == 1 :
        raise HTTPException(status_code=418,detail='city not found',headers={"Error_code":"ERROR"})
    return {"city_id": city_id}









