from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException

from . import models, schemas
from .utils import get_password_hash

def get_user(db:Session, user_id:int):
    return db.query(models.User).get(user_id)

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def get_users(db:Session, skip:int=0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user=schemas.UserCreate):
    
    hashed_password = get_password_hash(user.password)

    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_articles(db:Session, limit: int = 100, skip: int=0):
    return db.query(models.Artical).offset(skip).limit(limit).all()

def create_article(db:Session,article:schemas.ArticleCreate, user_id:int):
    db_item = models.Artical(**article.dict(),author_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_object_or_404(db:Session, Model:models.Base, object_id:int):
    db_object  = db.query(Model).filter(Model.id==object_id).first()
    if db_object is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_object

def update_article(db:Session, article_id: int, updated_fields: schemas.ArticleUpdate):
    db.execute(
        update(models.Artical)
        .where(models.Artical.id == article_id)
        .values(updated_fields.dict(exclude_unset=True))
    )
    db.flush()
    db.commit()
    return updated_fields

def delete_article(db:Session, article: schemas.Article):
    db.delete(article)
    db.commit()