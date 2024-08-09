from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import (
    text,
)  # text is from sql, you can add a query inside it if you want. kind of typecasting
from .database import Base
from sqlalchemy.orm import relationship

# this is sql alchemy model to design our table
# used to create, query and delete the entries in database

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
