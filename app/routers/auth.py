from fastapi import FastAPI, Response, status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from ..database import SessionLocal, engine ,get_db;
from .. import models, schema, utils, oauth2
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(

    tags=['Authentification']
)

@router.post("/login",response_model=schema.Token)
async def root(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    # user_credentials return
    # username 
    # password 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Invalid credential") 
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Invalid credential") 

    access_token = oauth2.craete_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}