# app/models/posts_table.py

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from app.config.database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.models.user_tables import User

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,index=True, nullable=False)
    title = Column(String(50), index=True, nullable=False)
    content = Column(String(250), nullable=True)
    published = Column(Boolean,nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    user_id= Column(Integer, ForeignKey(User.id,ondelete='CASCADE',
                                        onupdate='NO ACTION'),nullable=False)
    owner = relationship(User)  # this is used to take some data from "User" table according 
    # to the schema 
    
    