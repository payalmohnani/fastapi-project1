from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.User(**user.dict())
    # if user already exists raise error
    check_user = db.query(models.User).filter(models.User.email == new_user.email).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email id: '{new_user.email}' already exists.\n Login instead or try with another Email ID")

    # hash user given password and add user in db
    new_user.password = utils.hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# fetch user information by id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user
