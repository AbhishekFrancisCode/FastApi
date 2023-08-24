# import time
# from random import randrange
# from fastapi.params import Body
# from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='123456',cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Connection to the database failed ')
#         print("Error: ", error )
#         time.sleep(2)
# my_post = [{
#     "title":"sexy beach",
#     "content":"look for all the beaches",
#     "id" : 1
# },{
#     "title":"i ate pizza from dominos",
#     "content":"in naples",
#     "id" : 2
# }]
# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p['id'] == id:
#             return i      
# def update_index_post(index, post):
#     my_post.insert(index, post)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"} 
