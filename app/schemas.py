from datetime import datetime
from pydantic import BaseModel, EmailStr


# this is py-dyantic model pr schema and this is referred in path operations to shape the req body and response
# this is just a validation layer


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    """
    for example let's take create when we create a post/item 
    it will send us back the sqlalchemy model it's not a dict to make it work we are using this below config
    
    """

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr  # email str will validate particularly for valid email format
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
