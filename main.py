from fastapi import FastAPI, Query, Body
from pydantic import BaseModel, Field 
from typing import Optional
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
app = FastAPI()

class Item(BaseModel) : #이게 pydantic model임
    name : str
    description : Optional[str] = None #이렇게 작성하면 post method 에 이 field 없어도 가능
    price : float
    is_offer : bool = None

class Item2(BaseModel) : #Field를 이용해서 구체적인 제한 가능
    name : str = Field(..., title="Item Name", min_length=2, max_length=50)
    description : str = Field(None, description="The description of the item", max_length=200)
    price : float = Field(..., gt = 0, description= "The Price must be greater than zero")
    tag : List[str] = Field(default=[], alias = "item-tags") #default로 설정해놓으면 없어도 가능

class Image(BaseModel) :
    url : str 
    name : str

class Item3(BaseModel) : #nested 모델 -> image 안에 또 다른 class 가 존재한다. 
    name : str
    description : str
    image : Image


class Price(BaseModel) :
    name : str
    description : str = None
    price : float

def get_item_from_db(id) :
    return {
        "name" : "Simple Item",
        "description" : "A simple Description",
        "price" : 50.0,
        "dis_price" : 45.0 #이거는 안뜸 왜냐? response model을 price로 지정해놓아서
    }

@app.get('/')
def root() :
    return {"hello world"}

@app.get("/items/{item_id}", response_model=Price)
def read_item(item_id : int) :
    item = get_item_from_db(item_id)
    return item


@app.post("/items/")
def create_item(item:  Item) :
    return {"item" : item}

@app.post("/items2/")
def create_item2(item : Item2) :
    return {"item" : item}


@app.get("/html/", response_class=HTMLResponse) #요즘은 그냥 자동으로 변환해준다. 근데 기본은 이렇게 명시적으로 적어놓는게 맞음. 
def read_html() :
    return "<h1>THIS IS HTML</h1>"


@app.get("/users/")
def read_users(q : str = Query(None, max_length = 50)) :
    return {"q" : q}

@app.get("/info/")
def read_info(info : str = Query(None, description="정보를 입력해주세요")) :
    return {"info" : info}


# @app.get("/itmes3/") 
# def read_items(
#     string_qeury : str = Query(default= "default value", min_length=2, regex=)
# ) :
# return 

# @app.get("/itmes/{item_id}")
# def read_item(item_id : int)