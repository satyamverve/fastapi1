# app/models/votes_tables.py

from sqlalchemy import Column, ForeignKey, Integer
from app.config.database import Base
from sqlalchemy.ext.declarative import declarative_base
from app.models.user_tables import User
from app.models.posts_table import Post

Base= declarative_base()

class Vote(Base):
    __tablename__ = "votes"
    v_user_id= Column(Integer, ForeignKey(User.id,ondelete='CASCADE',
                                          onupdate='NO ACTION'),primary_key=True)
    v_post_id= Column(Integer, ForeignKey(Post.id,ondelete='CASCADE',
                                          onupdate='NO ACTION'),primary_key=True)  