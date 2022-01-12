from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from .. import models, schema ,oauth2
from sqlalchemy.orm.session import Session
from ..database import get_db;

router = APIRouter(
    prefix = "/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def CreatePost(vote :schema.Vote,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
   
    print('userrrrr',current_user.id)
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) 
    found_vote = vote_query.first() 
    print('found voteeeeeeeeeeeeeee',found_vote)
    if (vote.dir == 1) :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted in this post {vote.post_id}") 

        new_vote = models.Vote(post_id = vote.post_id,user_id=current_user.id)
        print('voteeeeeeeeeeeeeee',new_vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return  {"message" : "successfully added vote"} 
    else :
        if not found_vote :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted vote"}