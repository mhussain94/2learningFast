#To create class schemas for request body to be imported in the main file for example
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str  

#Response schema

class ShowBlog(Blog): #extending Blog pydantic model
    class Config():
        orm_mode = True # since response is orm