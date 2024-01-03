#app/oauth/oauth2.py

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.auth.auth_schema import TokenData
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from app.config.database import get_db
from app.models.user_tables import User
from app.data.data_class import settings

oauth2_schema= OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY --> used to authenticate the user credentials and it is anything long string 
#ALGORITHM  --> Here we use the HS256 algorithm
#EXPRESSION TIME --> To set how much time the user have to be logged in

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    #make a copy of data becacuse we don't want to touch and change the database
    to_encode=data.copy()
    
    # logic to set for how much time user have to be logged in
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    to_encode.update({"exp": expire, "email": to_encode.get("email")}) #use it to use email as username
    
    # convert user_id to string
    to_encode["user_id"] = str(to_encode.get("user_id"))
    
    #creating JWT token
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# yaha p jo "token" h wo ek string h kyuki genereted jwt token v ek string hota h
#jb token verify krna hota h(login k baad jo token generate hoga) i.e, access_token
# toh wahi generated access_token ko hm assign krenge "token" m jab koe current_user login krega
# then, at that time we compare "access_token" by assigning it in "token"(input in bearer type) 
# i.e, "token == access_token"
# if this condition satisfies tavi user access kr payega koe v db ka data

def verify_access_token(token: str, credentials_exceptions):
    
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")  #user_id is the variable from which we 
        #created the access_token 
        if id is None:   
            raise credentials_exceptions
        token_data=TokenData(id=id)  
    except JWTError:
        raise credentials_exceptions
    
    return token_data
    
def get_current_user(token:str = Depends(oauth2_schema),db : session = Depends(get_db) ):
    credentials_exceptions= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    #logic to get the db details(email-id, user, etc) of the current logged user
    token = verify_access_token(token, credentials_exceptions)
    user= db.query(User).filter(User.id == token.id).first()
    return user