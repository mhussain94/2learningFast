from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import model, schemas, database
from sqlalchemy.orm import Session
from . import token
from hashing import Hash



router= APIRouter(
    tags = ['authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user= db.query(model.User).filter(model.User.email == request.username).first() #searching db for user
    if not user:
        raise HTTPException(status_code= 404, detail=f'Invalid Credentials')
    if not Hash.verify(user.password, request.password): #comparing hashed and input password
        raise HTTPException(status_code= 404, detail=f'Incorrect Password Credentials')
    #generating access token
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}