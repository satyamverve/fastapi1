# app/modules/users_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_tables import User 
from app.dto.users_schema import UserCreate
import utils


def create_user(db: Session, user: UserCreate): #INSERT or CREATE
    
    #hash the password -- user.password
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    # print("hello")
    user= db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# def get_user_by_username(db: Session, username: str):
#     return db.query(User).filter(User.username == str(username))


def update_user(db: Session, user_id: int, user: UserCreate):
    #hash the password -- user.password
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")   


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
