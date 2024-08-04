from fastapi import FastAPI, Response, status, HTTPException  # importing the fast api package
from pydantic import BaseModel
import psycopg2  # importing the package for connecting the pgsql driver and pyhton d
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()  # creating a instance of FastAPI

# refer here for https://www.psycopg.org/docs/ 
# before executing don't forget to add the host, DB name, user and password

while True:
    try:
        # creating the connection with desired database
        con = psycopg2.connect(host="", database="", user="", password="", cursor_factory=RealDictCursor)
        cursor = con.cursor()
        print("Connection to DB successful ")
        break
    except Exception as error:
        print("Connection to database failed")
        print(f"{error}")
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None  # optional field with default value to be none


my_posts = [{"title": "title 1", "content": "content 1", "published": True, "rating": 4, "id": 1}]


def find_one(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/api/v1/posts")
async def get_posts():
    cursor.execute("""select * from posts""") # query to get all the data from posts table
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/api/v1/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        """insert into posts(title,content,published) values(%s,%s,%s) RETURNING * """, # query to add new post into the table
        (post.title, post.content, post.published),
    )

    new_post = cursor.fetchone()
    con.commit()
    return {"new_post": new_post}


@app.get("/api/v1/posts/{id}")
async def get_post(id: int):
    cursor.execute("""select * from posts where id=%s """, str(id)) # query to retrieve a data based on ID
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")


@app.put("/api/v1/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(
        """update posts set title = %s, content= %s, published= %s where id=%s returning *""", # query to update the post based on the id
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    con.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return {"status": "success", "data": updated_post}


@app.delete("/api/v1/posts/{id}")
async def delete_post(id: int):
    cursor.execute("""delete from posts where id=%s returning *""", str(id)) # query to delete the post based on the ID
    deleted_post = cursor.fetchone()
    con.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
