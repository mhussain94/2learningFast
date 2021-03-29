from fastapi import FastAPI, Depends, status, Response, HTTPException
import uvicorn
from pydantic import BaseModel
import schemas, model, hashing #Importing from the same directory
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()
model.Base.metadata.create_all(bind=engine) #intiating the db, to create the models(tables)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Depends to create connection to db by creating a get_db function
@app.post('/blog', status_code=201, tags=["Blog Methods"]) #status code for something created, tags for grouping on swagger
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = request.title, body = request.body)
    db.add(new_blog) #add the blog
    db.commit() # to persist changes on the db
    db.refresh(new_blog)
    return new_blog #return the blog

@app.delete('/blog', status_code=204, tags=["Blog Methods"])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found to be deleted') #does above 2 in same line
    return {'done'}

@app.put('/blog/{id}', status_code=202, tags=["Blog Methods"])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id) #query to check if blog exists
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'Blog with the id : {id} not found')
    blog.update({'title' : request.title, 'body': request.body}, synchronize_session=False) #query to update blog
    db.commit()
    return 'updated'
    


@app.get('/blog', response_model = List[schemas.ShowBlog], tags=["Blog Methods"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all() #model.Blog is the tablename!
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=["Blog Methods"])
def get_single_blog(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if blog != None:
        return blog
    elif blog == None:
        #response.status_code =400 #To generate custom responses!!, need to provide response:Response in params
        #return 'no blog found'
        raise HTTPException(status_code=400, detail=f'Blog with the id : {id} not found') #does above 2 in same line



@app.post('/user', tags=["User Methods"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = model.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)) #password input is the hashedPassword now from hashing schema.hash class. bcrypt method
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

if __name__ == '__main__': 
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)