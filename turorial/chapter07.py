'''
xunlian
'''
from enum import Enum
from random import random
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status,Request,Form,Header
from pydantic import BaseModel, Field
from pydantic import BaseModel
import uuid


app07 = APIRouter()



#data={"tom":{"UserName":"tom","password":"123456"},"james":{"UserName":"james","password":"James123"},"Brand":{"UserName":"Brand","password":"Brand()123"}}
data={"tom":{"UserName":"tom","password":"Ceshi123*","name":"汤姆","token":None,"age":"22","phoneNumber":"16618899875","question":{"对你影响最大的人是？":"汤姆","你的小学就读地是？":"中国","你的生辰属相是？":"狗"}},
      "james":{"UserName":"james","password":"James123","name":"詹姆斯","token":None,"age":"22","age":"33","phoneNumber":"16618897875","question":{"对你影响最大的人是？":"詹姆斯","你的小学就读地是？":"中国","你的生辰属相是？":"狗"}},
      "Brand":{"UserName":"Brand","password":"Brand123","name":"布莱恩特","token":None,"age":"22","age":"33","question":{"对你影响最大的人是？":"布莱恩特","你的小学就读地是？":"中国","你的生辰属相是？":"虎"}}}

final_token="hfj7dhkjf824dsuye8w14uyre7wnkjdh14jh7fdsfsjo"
class question(str,Enum):
    one = "对你影响最大的人是？"
    two = "你的小学就读地是？"
    three = "你的生辰属相是？"


class User(BaseModel):
    UserName:str
    # PassWord:Optional[str] = Field(
    #     ..., description="密码", max_length=16, example="12",regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[\da-zA-Z!@#$%^&*]{8,16}$'
    # )

class User_login(User):
    # UserName:str
    PassWord:Optional[str] = Field(
        ..., description="密码", max_length=16, example="12",regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[\da-zA-Z!@#$%^&*]{8,16}$'
    )

class UserNew(User):
    PassWord: Optional[str] = Field(
        ..., description="密码", max_length=16, example="12",
        regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[\da-zA-Z!@#$%^&*]{8,16}$'
    )

    newPassWord:Optional[str] = Field(
        ..., description="密码", max_length=16, example="12",regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[\da-zA-Z!@#$%^&*]{8,16}$'
    )



class User_detail(User):
    PassWord: Optional[str] =Field(
        ..., description="密码", max_length=16, example="12",regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[\da-zA-Z!@#$%^&*]{8,16}$'
    )
    name: str
    # age: Optional[str] = Field(
    #     None, description="年龄", max_length=3, example="12"
    # )
    age: Optional[str] = Field(
        ..., description="年龄", max_length=3, example="12"
    )
    questions: Optional[dict] = Field(
        ..., description="预留问题", example={"对你影响最大的人是？":"xxx","你的生辰属相是？":"老虎"}
    )

class User_info(User):

    name: str
    age: Optional[str] = Field(
        None, description="年龄", max_length=3, example="12"
    )
    questions: Optional[dict] = Field(
        ..., description="预留问题", example={"对你影响最大的人是？":"xxx","你的生辰属相是？":"老虎"}
    )

class User_reset_info(User_info):


    age: Optional[str] = Field(
        ..., description="年龄", max_length=3, example="12"
    )



#验证密码不能有特殊字符，必须有大小写

def get_uuid():
    get_randomnumber_uuid = uuid.uuid4()  # 根据 随机数生成 uuid , 既然是随机就有可能真的遇到相同的，但这就像中奖似的，几率超小，因为是随机而且使用还方便，所以使用这个的还是比较多的。
    return get_randomnumber_uuid

#注册用户
@app07.post("/register")
def register(User:User_detail):
    username=User.UserName
    if not username :
        return {"code":"400","message":"用户名不能为空！"}
    if username in data.keys():
        return {"code":"200","message":"用户注册成功！","userInfo":data["tom"]} #输入存在的用户名也不会报错
        # return {"code":"400","message":"用户名已存在！"}
    if not User.name:
        return {"code":"400","message":"真实姓名不能为空"}
    if not User.questions:
        return {"code":"400","message":"预留问题不能为空"}
    if  User.age == "":
        return {"code":"400","message":"年龄不能为空"}
    if User.age == None:
        User.age=""
    for x in User.questions.keys():
        if User.questions[x]=="":
            return {"code":"400","message":"预留问题不能为空"}
    # print(User.questions)
    # print(User.UserName)
    # print(type(User.UserName.strip()))
    data[User.UserName.strip()]={
    "UserName": User.UserName.strip(),
    "password": User.PassWord.strip(),
    "age":User.age.strip(),
    "name":User.name.strip(),
    "question":User.questions
  }
    return {"code":"200","message":"用户注册成功！","userInfo":data[User.UserName.strip()]}

#删除用户
@app07.post("/cancel/register")
def cancel_register(token:str=Header(None),UserName:str=Form(None),Password:str=Form(None)):

    username=UserName
    if not username or not username.strip():
        return {"code": "400", "message": "用户名不存在！"}#应提示用户名不能为空，当前提示用户名不存在
    if not Password or not Password.strip():
        return {"code": "400", "message": "密码不能为空！"}
    if not token or not token.strip():
        return {"code": "400", "message": "token不能为空！"}
    if username in data.keys():
        if token:
            print(token)
            print(data[username]["token"])
            print(data[username])
            if token != data[username]["token"]:
                return {"code": "400", "message": "无接口访问权限！"}
        else:
            return {"code": "400", "message": "无接口访问权限！"}
        if Password == data[username]["password"]:
            del data[username]
            return {"code":"200","message":"用户注销成功！"}
        return {"code":"400","message":"用户密码错误！"}
    else:
        return {"code": "400", "message": "用户名不存在！"}

#调取数据库数据
@app07.get("/getDataBaseData")
def getDataBaseData():
    return data

#找回密码
@app07.post("/reget/password")
def reget(User:User_reset_info):

    if User.UserName in data.keys():
        # if User.PassWord == data[User.UserName]["password"]:
            if User.name == data[User.UserName]["name"]:
                if User.age == data[User.UserName]["age"]:
                    keys = User.questions.keys()
                    for i in keys:
                        try:
                            if User.questions[i] == data[User.UserName]["question"][i]:
                                pass
                            else:
                                return {"code": "400", "message": "预留问题错误！"}
                        except (Exception) as e:
                            return {"code": "400", "message": "预留问题错误:" + str(e)}
                    return {"code": "200", "message": {"password": data[User.UserName]["password"]}}
                return {"code":"400","message":"年龄错误！"}
            return {"code":"400","message":"真实姓名错误！"}
        # return {"code": "400", "message": "用户密码错误！"}
    #return {"code": "400", "message": "预留问题错误！"} #用户不存在时返回预留问题错误
    return  {"code":"400","message":"用户不存在！"}


#修改密码
@app07.put("/modify/password")
def cancel_register(User:UserNew):
    username = User.UserName
    if username in data.keys():
        if User.PassWord == data[username]["password"]:
            data[username]["password"]=User.newPassWord
            return {"code":"200","message":"用户密码修改成功!"}
        #return {"code":"400","message":"用户不存在！"}#密码错误时返回用户不存在
        return {"code": "400", "message": "密码错误！"}
    return {"code": "400", "message": "用户不存在！"}

#登录
@app07.post("/login")
def login (User:User_login):

    username=User.UserName.strip()
    password=User.PassWord.strip()
    if not username:
        # return {"code":500,"message":"用户名不能为空"}
        return {"code": 500, "message": "用户名已登录"}#用户名为空时返回用户已登录
    if not password:
        # return {"code":500,"message":"密码不能为空"}
        return {"code": 500, "message": "密码超长"}#密码为空时返回密码超长
    if username in data.keys():
        userDict=data[username]
        if password==userDict["password"]:
            token=final_token+str(get_uuid())
            data[username]["token"]=token
            # return {"code":"200","message":"登录成功","userInfo":{"userName":username,"token":token}}
            return {"code": "200", "userInfo": {"userName": username, "token": token}}#登录成功时返回结构体同接口文档不同
        return {"code":500,"message":"用户名或密码错误"}
    # return {"code":500,"message":"密码错误！"} #用户名不存在时返回密码错误
    return {"code":500,"message":"用户名不存在"}

#获取登录身份信息
@app07.get("/get/UserInfo")
def get_UserInfo(token:str):
    keys=data.keys()
    for key in keys:
        if token == data[key]["token"]:
            return {"code":"200","userInfo":data[key]}
    return {"code":"200","userInfo":data["james"]} #输入错误token也会返回数据
    #return {"code":"200","message":"无法识别用户身份！请确认token正确性。"}
#测试接口
@app07.post("/test")
def login ():
    return {"message":"success"}

#测试新接口
@app07.post("/test/new")
def login ():
    return {"message":"success"}