from fastapi import FastAPI, Response, status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from app.utils import hash_Password
from .. import models, schema
from ..database import SessionLocal, engine ,get_db;

router = APIRouter(
    prefix = "/user",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
async def createUser(user :schema.CreateUser,db: Session = Depends(get_db)):
    # cur.execute("""insert into posts(title,content,published) values(%s, %s, %s) returning * """,(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    #  post_dic = post.dict()
    #  post_dic['id'] = randrange(0,10000000000000000) 
    #  myPostes.append(post_dic)
    hashed_Password = hash_Password(user.password)
    user.password = hashed_Password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user    

@router.get("/{id}",response_model=schema.UserOut)
async def getUser(id : int, response : Response,db: Session = Depends(get_db)):
    # print(type(id))
    # mypost = find_post(id)
    # cur.execute("""select * from posts where id = %s """,(str(id)))
    # post = cur.fetchone()
    # print(post)
    # if not post :
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 
    # return {"data":post} 
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user with {id} not found") 
    return user