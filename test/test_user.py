from fastapi.testclient import TestClient
from jose import jwt
import pytest
from app import schema
from app.config import settings
# from .database import client , session

def test_root(client):
    res = client.get("/")
    assert res.json().get('data') == 'successfull tata'
    assert res.status_code == 200  

def test_create_user(client):
    res = client.post("/user/", json={"email" : "titi@gmail.com","password":"123456"}) 

    newuser = schema.UserOut(**res.json())
    assert newuser.email == "titi@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login", data={"username" : test_user['email'] ,"password":test_user['password']}) 
    login_res = schema.Token(**res.json())
    payload =  jwt.decode(login_res.access_token,settings.secret_key,algorithms=settings.algorithm)   
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",
[
    ('sdfsfdsf@tata.com','123456',404),
    ('titi@gmail.com','123456',200),
    ('sdfsfdsf@tata.com','sdfdsdfdfs',404),
    (None,'123456',422), 
    ('sdfsfdsf@tata.com',None,422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/login", data={"username" : email ,"password":password}) 
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credential'