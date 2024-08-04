from .. import models
from fastapi import Response, status, HTTPException, Depends, APIRouter  # importing the fast api package
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import CreatePost, PostResponse

# since all the routes are same expect for those has ID we can use this prefix to define out route
# tags is simply to Group the fastapi route in the documentation here http://127.0.0.1:8000/docs/
router = APIRouter(prefix="/api/v1/posts", tags=["Posts"]) 

# we are sending list of posts so we are converting the post model to list of post model
@router.get("/", response_model=List[PostResponse])
# we have add this session as parameter to this function every-time
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post

# adding the model to the response we are getting from the server that is response_model=<model of the response>
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # referring the model that we created in model.py and adding the values in it like how we do in insert into query
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) - one way
    new_post = models.Post(
        **post.dict()
    )  # second method this is because what if we have more fields we can't type manually so we are unpacking the dict
    # adding to db
    db.add(new_post)
    # committing the change to the db
    db.commit()
    # kind of returning in raw sql what it does is we are retrieving the newly created post and storing it in the new_post
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    # using filter by to filter based on the key. the key can be any column name
    # db.query(models.Post).filter_by(id=str(id)).one() ---> you can try like this
    """
    filter_by is used for simple queries on the column names using regular kwargs, like

    db.users.filter_by(name='Joe')

    The same can be accomplished with filter, not using kwargs, but instead using the '==' equality operator,
    which has been overloaded on the db.users.name object

    db.users.filter(db.users.name=='Joe')

    You can also write more powerful queries using filter, such as expressions like

    db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
