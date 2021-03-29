#To create class schemas for request body to be imported in the main file for example
from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str  

class Blog(BlogBase): #Extending the above class
    class Config():
        orm_mode = True # since response is orm
    title: str
    body: str  


class User(BaseModel):
    name: str
    email: str  
    password: str

#Response model schema


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True # since response is orm
    

class ShowBlog(Blog): #extending Blog pydantic model
    title: str
    body:  str
    creator: ShowUser #to get the name and emial of the user in the response of getblog
