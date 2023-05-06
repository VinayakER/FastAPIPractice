from datetime import datetime
from sqlalchemy import Boolean, Integer, Column, ForeignKey, String,DateTime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255),unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    articles = relationship("Artical", back_populates="author", cascade="all,delete")

    def __repr__(self):
        return f"{self.email}"
    

class Artical(Base):
    __tablename__="articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    body = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(),onupdate=datetime.now())
    author_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User",back_populates="articles")

    def __repr__(self):
        return f"{self.title}"