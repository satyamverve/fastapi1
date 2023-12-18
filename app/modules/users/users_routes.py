# app/modules/users_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from app.dto.users_schema import UserCreate, UserOut # Update the import statement
from app.modules.users.users_service import create_user, get_user, update_user, delete_user #, get_user_by_username
from app.config.database import  get_db

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/{user_id}",response_model=UserOut)
def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)



# @router.get("/{username}")
# def read_user_by_username(username: str , db: Session = Depends(get_db)): #Path(...) means that parameter is required
#     user = get_user_by_username(db, username)
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"User with username {username} not found")
#     return {"db": user}


@router.put("/{user_id}")
def update_user_api(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
