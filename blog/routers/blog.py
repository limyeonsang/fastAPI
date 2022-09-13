from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(

)

get_db = database.get_db


@router.get('/blog', response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'incorret id {id}')

    blog.delete(synchronize_session=False)
    db.commit()
    return 'complete'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'incorrect id {id}')

    blog.update(request.dict())
    db.commit()
    return 'update success'


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def single_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'incorrect id {id}')

    return blog
