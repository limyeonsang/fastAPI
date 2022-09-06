from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def del_post(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'incorret id {id}')

    blog.delete(synchronize_session=False)
    db.commit()
    return 'complete'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'incorrect id {id}')

    blog.update(request.dict())
    db.commit()
    return 'update success'


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'incorrect id {id}')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'incorrect id {id}'}
    return blog


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'incorrect user id {id}')

    return user
