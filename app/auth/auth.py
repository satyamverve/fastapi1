#app/auth/app.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import session
from app.config.database import get_db
from app.models.user_tables import User
import utils
from app.oauth import oauth2
# from app.auth.auth_schema import UserAuth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter( )

@router.post('/login')

#now making the login by the help of fastapi inbuilt class(bydefault in payload it takes username and password)
def user_login(user_credentials : OAuth2PasswordRequestForm= Depends(), 
               db : session= Depends(get_db)):

    # user= db.query(User).filter(User.username == user_credentials.username).first()

    user = db.query(User).filter(User.email == user_credentials.username).first() #use this to login with email as username
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    # comparing the plain password(which was entered by user) with hashed password(stored in db)
    #and "verify" is the function which converts plain password in hashed for compariosion
    if not utils.verify(user_credentials.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid Credentials")
     
    #create token (remember this is the data(i.e, user_id) which we want to put in the payload)
    # This is totally on you ki kis column k  sath token generate krna h 
    
    access_token= oauth2.create_access_token(data= {"user_id" : user.id})
    

    return {"access_token": access_token, "token_type" : "bearer"} 
    #Here bearer is the the declaration where we put our token to validate
    
    
