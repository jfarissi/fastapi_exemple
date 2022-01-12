from fastapi.testclient import TestClient
import pytest
from app import models
from app.main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token


SQL_DATABASE_ALCHEMY_URL =  f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQL_DATABASE_ALCHEMY_URL)
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/user/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return 

@pytest.fixture
def test_user(client):
    user_data = {
        "email":"titi@gmail.com",
        "password":"123456"
    }
    res = client.post("/user/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }        
    return client


@pytest.fixture
def test_posts(test_user,session):
    post_data= [{
        "title":"post1",
        "content":"content1",
        "owner_id":test_user['id']
    },{
        "title":"post2",
        "content":"content2",
        "owner_id":test_user['id']
    },{
        "title":"post3",
        "content":"content3",
        "owner_id":test_user['id']
    },{
        "title":"post4",
        "content":"content4",
        "owner_id":test_user['id']
    }
    ]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model,post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    session.query(models.Post).all()
    return posts

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    print('new voteeeeeeeeeee',new_vote)
    session.add(new_vote)
    session.commit()
    session.query(models.Vote).all()
    return new_vote


