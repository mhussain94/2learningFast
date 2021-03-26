from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str  

@app.post('/blog')
def create(request: Blog):
    return {'data' : f'blog created with title : {request.title}, with body : {request.body}'}

if __name__ == '__main__': 
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)