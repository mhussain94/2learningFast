from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
import model, schemas, database

def get_all(db: Session):
    blogs = db.query(model.Blog).all() #model.Blog is the tablename!
    return blogs

def create_blog(request:schemas.Blog, db: Session):
    new_blog = model.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog) #add the blog
    db.commit() # to persist changes on the db
    db.refresh(new_blog)
    return new_blog #return the blog

def delete_blog(id, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found to be deleted') #does above 2 in same line
    return {'done'}

def update_blog(id, request: schemas.Blog, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id) #query to check if blog exists
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'Blog with the id : {id} not found')
    blog.update({'title' : request.title, 'body': request.body}, synchronize_session=False) #query to update blog
    db.commit()
    return 'updated'

def get_single_blog(id,response: Response, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if blog != None:
        return blog
    elif blog == None:
        #response.status_code =400 #To generate custom responses!!, need to provide response:Response in params
        #return 'no blog found'
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found') #does above 2 in same line