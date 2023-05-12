from typing import List, Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from . import crud, models, schemas
from .dependencies import get_db, oauth2_scheme, get_current_user
from .utils import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
import time
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # print(request.method)
    response = await call_next(request)
    # print(response)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Temp headers added for react
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return response

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session=Depends(get_db)):
    
    user = authenticate_user(db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub":user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/me", response_model=schemas.User)
def read_users_me(current_user:Annotated[schemas.User,Depends(get_current_user)]):
    return current_user

@app.post("/users/", response_model=schemas.User)
def create_user(user:schemas.UserCreate, current_user: Annotated[schemas.User, Depends(get_current_user)] , db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(token:Annotated[str, Depends(oauth2_scheme)], skip:int =0, limit: int=100, db:Session=Depends(get_db)):
    users=crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db:Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip:int = 0, limit: int=100, db:Session= Depends(get_db)):
    articles = crud.get_articles(db,skip=skip, limit=limit)
    print(articles)
    return articles

@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id:int, db:Session = Depends(get_db)):
    return crud.get_object_or_404(db, models.Artical,object_id=article_id)

@app.post(
    "/articles/",
    response_model=schemas.Article,
    status_code=status.HTTP_201_CREATED
)
def create_user_article(article:schemas.ArticleCreate, current_user : Annotated[schemas.User,Depends(get_current_user)], db: Session=Depends(get_db)):
    return crud.create_article(db=db,user_id=current_user.id, article=article)

@app.patch("/articles/{article_id}", response_model=schemas.ArticleUpdate)
def update_article(article_id:int,updated_fileds: schemas.ArticleUpdate,db:Session=Depends(get_db)):
    return crud.update_article(db, article_id, updated_fileds)
