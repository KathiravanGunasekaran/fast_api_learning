from .. import models, utils
from fastapi import Response, status, HTTPException, Depends, APIRouter  # importing the fast api package
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..schemas import User, UserResponse


router = APIRouter()


@router.get("/api/v1/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post(
    "/api/v1/user",
    status_code=status.HTTP_201_CREATED,
)
# db: Session = Depends(get_db) -> creating the session dependency
def register_user(user: User, db: Session = Depends(get_db)):
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "message": f"A new user with {new_user.email} registered"}


@router.get("/api/v1/user/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")


@router.delete("/api/v1/user/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
not needed for now, need a patch call rather than doing put here I guess

@router.put("/api/v1/user/{id}", response_model=UserResponse)
def update_user(id: int, updated_user: User, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
"""
