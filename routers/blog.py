from fastapi import APIRouter, Depends, status, HTTPException, Response
import model, schemas, database
from sqlalchemy.orm import Session
from typing import List

get_db = database.get_db

router = APIRouter()

@router.get('/blog', response_model = List[schemas.ShowBlog], tags=["Blog Methods"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all() #model.Blog is the tablename!
    return blogs

#Depends to create connection to db by creating a get_db function
@router.post('/blog', status_code=201, tags=["Blog Methods"]) #status code for something created, tags for grouping on swagger
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog) #add the blog
    db.commit() # to persist changes on the db
    db.refresh(new_blog)
    return new_blog #return the blog

@router.delete('/blog', status_code=204, tags=["Blog Methods"])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found to be deleted') #does above 2 in same line
    return {'done'}

@router.put('/blog/{id}', status_code=202, tags=["Blog Methods"])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id) #query to check if blog exists
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'Blog with the id : {id} not found')
    blog.update({'title' : request.title, 'body': request.body}, synchronize_session=False) #query to update blog
    db.commit()
    return 'updated'
    

@router.get('/blog/{id}', status_code=200, response_model=schemas.Blog, tags=["Blog Methods"])
def get_single_blog(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if blog != None:
        return blog
    elif blog == None:
        #response.status_code =400 #To generate custom responses!!, need to provide response:Response in params
        #return 'no blog found'
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found') #does above 2 in same line