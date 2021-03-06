from fastapi import FastAPI
import uvicorn
import model #Importing from the same directory
from database import engine
from routers import blog, user, authentication

app = FastAPI()
model.Base.metadata.create_all(bind=engine) #intiating the db, to create the models(tables)

app.include_router(authentication.router)
app.include_router(blog.router) #getting the routers. @router.get from routing the apis
app.include_router(user.router) # remove , tags=["User Methods"] from apis and adding here

if __name__ == '__main__': 
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)