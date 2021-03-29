from fastapi import APIRouter, Depends, HTTPException, status
import model, schemas, database
from sqlalchemy.orm import Session
from hashing import Hash



router= APIRouter(
    tags = ['authentication']
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user= db.query(model.User).filter(model.User.email == request.username).first() #searching db for user
    if not user:
        raise HTTPException(status_code= 404, detail=f'Invalid Credentials')
    if not Hash.verify(user.password, request.password): #comparing hashed and input password
        raise HTTPException(status_code= 404, detail=f'Incorrect Password Credentials')
    return user