from fastapi import APIRouter, Depends, status, Response
import model, schemas, database
from sqlalchemy.orm import Session
from typing import List
from repository import blogRepo


get_db = database.get_db

router = APIRouter(
    prefix= '/blog',
    tags=['blogs']
)

@router.get('/', response_model = List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    return blogRepo.get_all(db) #function taken to repository/blog.py and now called here

#Depends to create connection to db by creating a get_db function
@router.post('/', status_code=201 ) #status code for something created, tags for grouping on swagger
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepo.create_blog(request, db) #function taken to repository/blog.py and now called here

@router.delete('/', status_code=204)
def delete(id, db: Session = Depends(get_db)):
    return blogRepo.delete_blog(id, db)

@router.put('/{id}', status_code=202)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepo.update_blog(id, request, db)
    

@router.get('/{id}', status_code=200, response_model=schemas.Blog)
def get_single_blog(id,response: Response, db: Session = Depends(get_db)):
    return blogRepo.get_single_blog(id, response ,db)