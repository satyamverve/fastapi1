# app/modules/posts_routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.modules.posts.posts_service import create_post, get_post, update_post, delete_post, get_all_posts, pagination
from app.config.database import get_db
from app.dto.posts_schema import PostCreate, Post_Return#, PostJoin
from typing import List
from app.oauth import oauth2
from typing import Optional

router = APIRouter()

@router.get("/all/",response_model=List[Post_Return])
# @router.get("/all/",response_model=List[PostJoin])
def all_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    return get_all_posts(db, current_user)


#pagination and searching
@router.get("/all/search", response_model=List[Post_Return])
def search_post_keyword(Limit: int = 10, skip: int = 0, db: Session = Depends(get_db),
                 search:Optional[str]="",
                 current_user: int = Depends(oauth2.get_current_user)):
    return pagination(Limit, skip, db, search, current_user)



# #response_model is used to filter and validate the response data
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Post_Return) 
# def create_new_post(post: PostCreate, db: Session = Depends(get_db)):


# Here we are using a function called get_current_user to set that ki jab user logged-in hoga 
# tavi post create kar payega 
def create_new_post(post: PostCreate, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.username)
    return create_post(db, post,current_user)


@router.get("/{post_id}",response_model=Post_Return)
def read_post(post_id: int, db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    return get_post(db, post_id)



@router.put("/{post_id}",response_model=Post_Return)
def update_post_api(post_id: int, post: PostCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    return update_post(db, post_id, post,current_user)


@router.delete("/{post_id}",response_model=Post_Return)
def delete_post_api(post_id: int, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    return delete_post(db, post_id,current_user)
