from sys import prefix
from typing import List, Optional
from fastapi import FastAPI, Response, status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import func, mode
from app import oauth2
from app.utils import hash_Password
from .. import models, schema
from ..database import SessionLocal, engine ,get_db;

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

@router.get("/")
async def getPost(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
                 limit : int = 10, skip : int = 0,searsh : Optional[str] = ""):
    #  cur.execute("""select * from posts """)
    #  posts = cur.fetchall()
    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(searsh)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter = True).group_by(
        models.Post.id).filter(models.Post.title.contains(searsh)).limit(limit).offset(skip).all()
    
    # print(posts)

    return posts

@router.get("/{id}",response_model=schema.PostOut)
async def getPost(id : int, response : Response,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # print(type(id))
    # mypost = find_post(id)
    # cur.execute("""select * from posts where id = %s """,(str(id)))
    # post = cur.fetchone()
    # print(post)
    # if not post :
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 
    # return {"data":post} 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter = True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    # print(posts)
    if not posts :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 


    return posts    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with {id} not found"}
        # return {"post detail": mypost}    

# @router.get("/posts/latest")
# async def getPost(id : int):
#     print(type(id))
#     lastpost = myPostes[len(myPostes) - 1]
#     return {"post detail": lastpost}   

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
async def CreatePost(post :schema.CreatePost,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute("""insert into posts(title,content,published) values(%s, %s, %s) returning * """,(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    #  post_dic = post.dict()
    #  post_dic['id'] = randrange(0,10000000000000000) 
    #  myPostes.append(post_dic)
    print(current_user)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Post(id : int, response : Response,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute("""delete from posts where id = %s returning * """,(str(id)))
    # deleted_post = cur.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    delete_post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(posts)
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the action") 

    db.delete(delete_post)
    db.commit()
    # return {"data":delete_post}    
    # myPostes.pop(index)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with {id} not found"}
    return Response(status_code = status.HTTP_204_NO_CONTENT)        


@router.put("/{id}", response_model=schema.Post)
async def update_Post(id : int,post : schema.CreatePost, response : Response,
                      db: Session = Depends(get_db)
                      ,current_user:int=Depends(oauth2.get_current_user)):

    # index = find_index_post(id)
    # cur.execute("""update posts set title = %s,content = %s, published = %s where id = %s returning * """,(post.title,post.content,post.published, str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_u = updated_post.first()
    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 
    if post_u != None :
        if post_u.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the action") 
    # myPostes.pop(index)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} not found") 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with {id} not found"}
    # print(post)
    # post_dict = post.dict()
    # post_dict['id'] = id
    # myPostes[index] = post_dict    
    updated_post.update(post.dict())
    db.commit()
    return  updated_post.first()