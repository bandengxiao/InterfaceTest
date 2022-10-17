from fastapi import APIRouter , Path ,Query ,Cookie,Header
from typing import Optional,List
from enum import Enum
from pydantic import BaseModel,Field
from datetime import datetime
app03 = APIRouter()

##### Path（用于验证路径参数） 、Query（用于验证查询参数）、Field（用于验证请求体参数）

@app03.get('/get/paramters')   #如果下面这个函数（相同路由）传入参数为 paramters，那么会走到第一个函数来，因为拼接到路径上和第一个函数路径相同，函数顺序就是路由顺序
def getParamters():
    return {'return':'this is a messageaaa'}

@app03.get('/get/{paramters}')
def getParamters(paramters:Optional[str]=None):
    return {'return':paramters}

class CityName(str , Enum):  #定义枚举类
    BeiJing = "Beijing China"
    ShangHai = "ShangHai China"

@app03.get("/enum/{city}")
def getLatest(city:CityName):
    if city == CityName.ShangHai:
        return {"city":CityName.ShangHai,"confirmed":1492}
    if city == CityName.BeiJing:
        return {"city":CityName.BeiJing,"confirmed":1000}
    return {"city":city,"confirmed":"unknow"}

@app03.get("/file/{file_path:path}")
def getFile(file_path:str):
    return f"the file Path is {file_path}"

@app03.get('/path_/{num}')
def path_params_validate(
        num : int = Path(...,title="You number",description="不可描述",ge=1,le=10)
):
    return num


#查询参数和字符串的验证

@app03.get('/query')
def page_limit(page:int,limit:Optional[int]=None): #给了默认值就是选填参数，没给默认值就是必填参数
    if limit :
        return {"page":page,limit:limit}
    return {"page":page}


@app03.get("/query/bool/conversion")
def type_conversion(param:bool = False): #bool类型转换  yes  on  1 会转换为true
    return param

@app03.get('/query/validations')
def query_params_validation(value:str = Query(...,min_length=8,max_length=16,regex="^a"),
                            values:List[str] = Query(["A1","A2"],alias="alias_name")
                            ):
    return value,values



### 请求体和字段
class CityInfo(BaseModel):
    name : str = Field(...,example='beijing')
    country : str
    country_code : str=None
    country_population : int =Field(default=800,title="人口数量",description="国家的人口数量",ge=800)


    class Config:
        schema_extra={
            "name":"beijing ",
            "country":"china",
            "country_code":"CN",
            "country_population":14000000
        }

@app03.post('/request_body/city')
def city_info(city:CityInfo):
    print(city.name,city.country)
    return city.dict()

### 多参数混合使用   ##### Path（用于验证路径参数） 、Query（用于验证查询参数）、Field（用于验证请求体参数）

@app03.put('/request_body/city/{name}')
def mix_city_info(
                        #python中带默认值的，必须作为后面的参数
        city01:CityInfo,
        city02:CityInfo,
        confirmed : int = Query(ge=0,description="确诊数",default=0),
        death : int =Query(ge=0,description="死亡数",default=0),
        name : str = Path(...,description="测试name"),

):
    if name == "shanghai":
        return {"name":name}
    return city01.dict(),city02.dict()


# 数据格式嵌套的请求体

class Data(BaseModel):
    city:List[CityInfo]=None #这里就是定义数据格式类型嵌套的请求体
    date:datetime
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    death: int = Field(ge=0, description="死亡数", default=0)

@app03.put('/request_body/nested')
def nested_modles(data:Data):
    return data.dict()

# Cookie 和 Header参数

@app03.get('/cookies')
def cookie(cookie_id : Optional[str]=Cookie(None)):
    return {"cookie_id":cookie_id}

@app03.get("/header")
def header(user_agent:Optional[str]=Header(None,convert_underscores=True),x_token:List[str]=Header(None)):
    """
    有些http或web服务器是不允许请求头中带下划线的，所以Header提供convert_underscores属性设置
    :param user_agent:
    :param x_token:
    :return:
    """

    return {"user_agent":user_agent,"x_token  ":x_token}




