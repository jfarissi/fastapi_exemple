from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column, Integer , String, Boolean

class Post(Base):
    __tablename__ = "posts"
 
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,default=True, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('Now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner  = relationship("User")


class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('Now()'))

class Vote(Base):
    __tablename__ = "votes"
 
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), nullable=False,primary_key=True)