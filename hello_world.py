
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI() #这里不一定是app，可以是任意名称

class CityInfo(BaseModel):
    province : str
    country : str
    is_affected : Optional[bool]=False

@app.get("/")
async def hello_world():
    return {"hello":"world"}
@app.get("/city/{city}")  # http://127.0.0.1:8000/city/beijing?query_string=ceshi
async def result(city:str,query_string:Optional[str] = None):
    return {"city":city,"query_string":query_string}

@app.put("/city/{city}")
async def result(city:str,city_info:CityInfo):
    return {'city':city,"province":city_info.province,"country":city_info.country,"is_affected":city_info.is_affected }



#启动命令 uvicorn hello_world:app --reload