from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
import model, schemas, database, hashing

def create_user(request: schemas.User, db: Session):
    new_user = model.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)) #password input is the hashedPassword now from hashing schema.hash class. bcrypt method
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id:int,response: Response , db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with the id : {id} not found')
    return user