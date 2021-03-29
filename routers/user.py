from fastapi import APIRouter, Depends, status, Response
import model, schemas, database
from sqlalchemy.orm import Session
from repository import userRepo


get_db = database.get_db

router = APIRouter( 
    tags=['users'], #default tags have been added here instead of each api initiation
    prefix='/user'  #default end point prefix for all APIs
)

@router.post('/', response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return userRepo.create_user(request,db)

@router.get('/{id}', response_model= schemas.ShowUser)
def get_user(id:int,response: Response , db: Session = Depends(get_db)):
    return userRepo.get_user(id, response, db)