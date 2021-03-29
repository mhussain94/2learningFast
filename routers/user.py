from fastapi import APIRouter, Depends, status, HTTPException, Response
import model, schemas, database, hashing
from sqlalchemy.orm import Session
from typing import List

get_db = database.get_db

router = APIRouter()

@router.post('/user', response_model= schemas.ShowUser, tags=["User Methods"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = model.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)) #password input is the hashedPassword now from hashing schema.hash class. bcrypt method
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', response_model= schemas.ShowUser, tags=["User Methods"])
def get_user(id:int,response: Response , db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with the id : {id} not found')
    return user