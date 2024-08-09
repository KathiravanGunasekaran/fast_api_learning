from .. import models
from fastapi import Response, status, HTTPException, Depends, APIRouter  # importing the fast api package
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import CreatePost, PostResponse
from ..oauth2 import get_current_user

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

"""
# we are sending list of posts so we are converting the post model to list of post model

# we have add this session as parameter to this function every-time it's a dependency injection that we are doing
"""


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 10):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).all()
    return post


"""
adding the model to the response we are getting from the server that is response_model=<model of the response>

referring the model that we created in model.py and adding the values in it like how we do in insert into query
new_post = models.Post(title=post.title, content=post.content, published=post.published) - one way

"""

"""
- we need to expand the post that's coming from client to dict because
at first it will look like this -> title='fourth 1' content='Hey I am fourth' published=False
but when we expand by post.dict() or post.model_dump it will become a dictionary
- then we need to add it to DB
- commit the changes to DB
- refresh the DB and put the changes in new_post variable 
here in background it does the returning sql functionality. that's why you are getting the created post response

"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""
filter_by is used for simple queries on the column names using regular kwargs, like
db.users.filter_by(name='Joe')
The same can be accomplished with filter, not using kwargs, but instead using the '==' equality operator,
which has been overloaded on the db.users.name object
db.users.filter(db.users.name=='Joe')
You can also write more powerful queries using filter, such as expressions like
db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))

using filter by to filter based on the key. the key can be any column name
db.query(models.Post).filter_by(id=str(id)).one() ---> you can try like this
"""


@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id).first()
    if post:
        return post
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")


@router.put("/{id}", response_model=PostResponse)
async def update_post(
    id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform any actions")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform any actions")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
