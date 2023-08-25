from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_users)):
    posts = db.query(models.Post).all()
    print(current_user)
    return posts

@router.get("/{id}", status_code= status.HTTP_404_NOT_FOUND, response_model=schemas.PostResponse)
def get_post_id(id : int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_users)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Id -> {id} not found in the database")
    return post 

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
        # post_dist = post.model_dump()
        # post_dist['id'] = randrange(1,1000000)
        # my_post.routerend(post_dist)
        new_post = models.Post(**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    post = db.query(models.Post).filter(models.Post.id == id)
    # index = find_index_post(id)
    # print(index)
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Id -> {id} not found in the database")
    # my_post.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}",response_model=schemas.PostResponse)
def update_post(id : int, updated_post : schemas.UpdatePost, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Id -> {id} not found in the database")
    post_query.update(updated_post.model_dump() ,synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_post.pop(index)
    # my_post.insert(index, post_dict)
    return post_query.first() 

