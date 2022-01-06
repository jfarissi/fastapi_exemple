from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schema import Vote
from . import models
from .database import  engine;
from . import models
from .routers import post,user,auth,vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myPostes = [{"title":"title post 1","content":"content post 1","id":1},
             {"title":"title post 2","content":"content post 2","id":2}]   

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def test_postes():
    return {"data":"successfull tata"}

