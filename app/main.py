from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel): 
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{
    "title":"sexy beach",
    "content":"look for all the beaches",
    "id" : 1
},{
    "title":"i ate pizza from dominos",
    "content":"in naples",
    "id" : 2
}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

def update_index_post(index, post):
    my_post.insert(index, post)

@app.get("/")
def root():
    return {"message": "Hello World"} 

@app.get("/posts")
def get_all_posts():
        return {"data": my_post } 

@app.post("/posts")
def create_posts(post: Post):
        post_dist = post.model_dump()
        post_dist['id'] = randrange(1,1000000)
        my_post.append(post_dist)
        return {"data": my_post } 

@app.get("/posts/{id}", status_code= status.HTTP_404_NOT_FOUND)
def get_post_id(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Id -> {id} not found in the database")
    return {"post details": post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    print(index)
    if not index:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Id -> {id} not found in the database")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/posts/{id}")
def update_post(id : int, post : Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Id -> {id} not found in the database")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_post.pop(index)
    my_post.insert(index, post_dict)
    return {"post details": my_post} 