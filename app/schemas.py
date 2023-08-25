from pydantic import BaseModel, EmailStr

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase): 
    pass

class UpdatePost(PostBase): 
    pass

class PostResponse(BaseModel): 
    title: str
    content: str
    published: bool
    
    class Config:
        from_attributes = True

class CreateUser(BaseModel): 
    email: EmailStr
    password: str
    
class UserResponse(BaseModel): 
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel): 
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
     username: str | None = None
