# app/dto/posts_schema.py

from pydantic import BaseModel
from datetime import datetime
from .users_schema import UserOut

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  


class PostCreate(PostBase):
    pass

    
class Post_Return(PostBase):
    id : int
    created_at : datetime
    user_id: int
    owner: UserOut #owner was the variable used in "posts_table" for making relationship
    # between user and post table 
    
    # It simplifies the process of handling 
    # data validation and conversion between web request data and database models.
    class config:
        orm_mode=True
        
#This means that you can use instances of PostReturn to interact with a FastAPI 
# application that uses SQLAlchemy to interact with a database, and Pydantic will
# handle the data validation and conversion automatically.

# class PostJoin(PostBase):
#     Post_Return: Post_Return
#     votes: int
#     class config:
#         orm_mode=True
        
