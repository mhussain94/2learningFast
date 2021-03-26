from fastapi import FastAPI, Depends, status, Response
import uvicorn
from pydantic import BaseModel
import schemas, model #Importing from the same directory
from database import SessionLocal, engine
from sqlalchemy.orm import Session


app = FastAPI()
model.Base.metadata.create_all(bind=engine) #intiating the db, to create the models(tables)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Depends to create connection to db by creating a get_db function
@app.post('/blog', status_code=201) #status code for something created
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = request.title, body = request.body)
    db.add(new_blog) #add the blog
    db.commit()
    db.refresh(new_blog)
    return new_blog #return the blog

@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all() #model.Blog is the tablename!
    return blogs

@app.get('/blog/{id}', status_code=200)
def get_single_blog(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if blog != None:
        return blog
    elif blog == None:
        response.status_code =400 #To generate custom responses!!, need to provide response:Response in params
        return 'no blog found'

if __name__ == '__main__': 
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)