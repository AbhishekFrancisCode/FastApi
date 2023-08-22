from typing import Optional
from fastapi import FastAPI
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
    "title":"i ate pizza",
    "content":"in naples",
    "id" : 2
}]

@app.get("/")
def root():
    return {"message": "Hello World"} 

@app.get("/posts")
def create_posts():
        return {"data": my_post } 

@app.post("/posts")
def create_posts(post: Post):
        post_dist = post.model_dump()
        post_dist['id'] = randrange(1,1000000)
        my_post.append(post_dist)
        return {"data": my_post } 

@app.get("/posts/{id}")
def get_post(id):
        print(id)
        return {"post details": f"Heare is post {id}" } 