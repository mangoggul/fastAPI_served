from fastapi import FastAPI, Query
from pydantic import BaseModel, Field 
from typing import Optional
from typing import List
from fastapi.responses import HTMLResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import joblib

# FastAPI 인스턴스 생성
app = FastAPI()

# 샘플 데이터셋 생성 (여기서는 가상의 데이터 사용)
data = {
    'email': [
        'Congratulations! You have won a lottery.',
        'Dear friend, I am writing to you regarding...',
        'Free access to the best online courses!',
        'Meeting at 10 AM tomorrow.',
        'Get paid to work from home.',
        'Don’t forget to attend the team meeting.',
        'You are selected for a special prize!',
        'Please find the attached report.',
        'Claim your free gift now!',
        'Let’s catch up for coffee next week.',
        '축하합니다! 당신은 복권에 당첨되었습니다.',
        '친애하는 친구, 당신에게 연락 드립니다...',
        '최고의 온라인 강좌에 무료로 접근하세요!',
        '내일 오전 10시에 회의가 있습니다.',
        '재택근무로 돈을 벌 수 있습니다.',
        '팀 회의에 꼭 참석하세요.',
        '특별 상품이 선정되었습니다!',
        '첨부된 보고서를 확인해 주세요.',
        '지금 무료 선물을 신청하세요!',
        '다음 주에 커피 한 잔 하실래요?'
    ],
    'label': [
        'spam', 'ham', 'spam', 'ham', 'spam',
        'ham', 'spam', 'ham', 'spam', 'ham',
        'spam', 'ham', 'spam', 'ham', 'spam',
        'ham', 'spam', 'ham', 'spam', 'ham'
    ]
}

# DataFrame 생성
df = pd.DataFrame(data)

# 특징과 레이블 분리
X = df['email']
y = df['label']

# 데이터 전처리: 텍스트를 벡터로 변환
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# 의사결정 트리 모델 생성 및 학습
model = DecisionTreeClassifier(random_state=42)
model.fit(X_vectorized, y)

# 모델과 벡터라이저를 파일로 저장
joblib.dump(model, 'spam_classifier.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')

# Pydantic 모델 정의
class Email(BaseModel):
    content: str

# API 엔드포인트 정의
@app.post("/predict/")
async def predict(email: Email):
    # 이메일 텍스트 벡터화
    vectorizer = joblib.load('vectorizer.joblib')
    model = joblib.load('spam_classifier.joblib')
    email_vectorized = vectorizer.transform([email.content])
    
    # 예측 수행
    prediction = model.predict(email_vectorized)
    
    return {"prediction": prediction[0]}


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