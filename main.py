from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import schemas, model #Importing from the same directory
from database import SessionLocal, engine



app = FastAPI()
model.Base.metadata.create_all(bind=engine) #intiating the db, to create the table


@app.post('/blog')
def create(request: schemas.Blog):
    return {'data' : f'blog created with title : {request.title}, with body : {request.body}'}

if __name__ == '__main__': 
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)