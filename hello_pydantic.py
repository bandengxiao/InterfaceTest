from pydantic import BaseModel , ValidationError ,constr
from datetime import datetime
from typing import  List , Optional
from pathlib import Path
from sqlalchemy import Column,Integer,String
from sqlalchemy.dialects.postgresql import  ARRAY
from sqlalchemy.ext.declarative import declarative_base


class User (BaseModel):
    id : int # 如果没有给默认值就是必填字段
    name : str = "zhoumanzeng" #有默认值就是选填字段
    sign_up : Optional[datetime] = None #不填可以使用optional，后面接默认值
    friends : List[str] = [] #列表中的元素要是int类型，或者可以直接转换为int类型


external_data={
    "id":"1",
    "name":"zhou",
    "sign_up":2022-12-22,
    "friends":["wang","zhao"]
}


user=User(**external_data)
print(user.friends) ##实例化后调用属性
print(user.id)
print(user.name)
print(user.sign_up)


#################################################   json格式化错误信息
try:
    User(id="1",name="zhou",sign_up=2022-12-22,friends=["wang"])
except ValidationError as e: #ValidationError为pydantic库导入
    print(e.json()) #错误信息json格式化

################################################   模型类的属性和方法


print(user.dict()) #返回字典格式数据
print(user.json()) #返回json格式数据
print(user.copy()) #这里是浅拷贝 copy方法也是有返回值的
print(User.parse_obj(obj=external_data))#解析字典，解析后可赋值调用
# a = User.parse_obj(obj=external_data)
# print(a.friends)

raw_external_data='{"id":"1","name":"zhou","sign_up":"2022-12-22 12:22","friends":["wang","cai"]}'
print(User.parse_raw(raw_external_data)) #这个方法dateTime必须有时间 12:22 ，否则会报错，原因不详

path= Path('pydantic.json')#这个类需要了解一下
path.write_text(raw_external_data)
print(User.parse_file(path))#解析文件,返回User实例对象


print(user.schema())#这两个展示信息更多
print(user.schema_json())

external_data_error={
    "id":"测试",
    "name":"zhou",
    "sign_up":"2022-12-22 12:22",
    "friends":["wang","zhao"]
}
print(User.construct(**external_data_error)) #不检查数据，直接创建模型类，不建议在construct方法中传入未经验证的数据

print(User.__fields__.keys()) # 输出User模型类所有属性，定义模型类时，所有字段都注明类型，字段顺序就不会乱

################################## 递归模型

class Sound(BaseModel):
    sound:str
class Dog(BaseModel):
    birthday:datetime
    weight:float = Optional[None]
    sound : List [Sound]  #递归模型就是指一个嵌套一个
dogs=Dog(birthday=datetime.now(),weight=12.5,sound=[{"sound":"wang wang"},{"sound":"duang duang"}])

print(dogs.json())

###### ORM模型 ：从类实例创建符合ORM对象的模型

Base=declarative_base()

class CompanyOrm(Base):
    __tablename__ = 'company'
    id = Column(Integer,primary_key=True,nullable=False)
    public_key=Column(String(20),index=True,nullable=False,unique=True)
    name = Column(String(63),unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
     id : int
     public_key:constr(max_length=20)
     name:constr(max_length=63)
     domains:List[constr(max_length=255)]
     class Config:
         orm_mode=True

co_orm=CompanyOrm(
    id = 123,
    public_key="Testing",
    name="Testing",
    domains=["www.baidu.com","www.taobao.com"]
)
print(CompanyMode.from_orm(co_orm))