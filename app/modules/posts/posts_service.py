# app/modules/posts_service.py

from sqlalchemy.orm import Session
from app.models.posts_table import Post
from app.dto.posts_schema import PostCreate
from fastapi import HTTPException, status, Depends
from app.oauth import oauth2
from typing import Optional
from app.config.database import get_db
from app.models.votes_table import Vote
from sqlalchemy import func


def get_all_posts(db: Session, 
                  current_user: int = Depends(oauth2.get_current_user)): # -> List[Post]
    
    # #driver code to get all posts only of the logged in person
    # posts= db.query(Post).filter(Post.user_id == current_user.id).all()
    
    #code to get all posts of every users
    posts= db.query(Post).all()
    return posts
    
    
    #code to perform a join query to get specific combination of data of all posts
    # by default alchemy uses LEFT INNER JOIN, Here:"Post" is Left table and 
    # "Vote" is right table,, "label" is used for "ALIAS" and "func" is a alchemy functions 
    # used to perform operations like "count"
    
    # result=db.query(Post,func.count(Vote.v_post_id).label('votes')).join(
    #     Vote,Vote.v_post_id==Post.id, isouter=True).group_by(Post.id).all()
    
    # print(result)
    # return result
    
 


#driver code to limit the posts to display on a single page which also called pagination
#and search funtionality
def pagination(Limit: int = 10, skip: int = 0, db: Session = Depends(get_db),
               search:Optional[str]="" ,
               current_user: int = Depends(oauth2.get_current_user)):
    page = db.query(Post).filter(Post.title.contains(search)).limit(Limit).offset(skip).all()
    return page
    

def create_post(db: Session, post: PostCreate, 
                current_user: int = Depends(oauth2.get_current_user)):
    db_post= Post(user_id=current_user.id,**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post



def get_post(db: Session, post_id: int):
    all_post= db.query(Post).filter(Post.id==post_id).first()
    if all_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not found')
    else:
        return all_post

def update_post(db: Session, post_id: int, post: PostCreate,
                current_user: int = Depends(oauth2.get_current_user)):
    db_post= db.query(Post).filter(Post.id == post_id).first()
                
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not found')

    # #logic for only the logged in user can do any CRUD opeartions with only their own posts
    # if db_post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Not Authorized to perform requested action")   
    
    else:
        for key, value in post.model_dump(exclude_unset=True).items():
            setattr(db_post,key,value)
        db.commit()
        db.refresh(db_post)
        return db_post
        

def delete_post(db: Session, post_id: int,
                current_user: int = Depends(oauth2.get_current_user)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
       
    # #logic for only the logged in user can do any CRUD opeartions with only their own posts 
    # if db_post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Not Authorized to perform requested action") 
        
    else:
        db.delete(db_post)
        db.commit()
        return db_post
        
