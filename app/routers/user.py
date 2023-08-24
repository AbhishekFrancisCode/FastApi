from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_sers(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hash_password = utils.Hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_404_NOT_FOUND, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user dose't exist")
    return user