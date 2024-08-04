from fastapi import FastAPI, Response, status, HTTPException  # importing the fast api package
from pydantic import BaseModel
from random import randrange

app = FastAPI()  # creating a instance of FastAPI


"""
- decorator to specify a get(read) method of CRUD (Create Read Update Delete),
it can be any method like post(create), patch(update), put(update) and delete
this is the place where we specify the route/endpoint/url of the api

refer this - https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

- a function definition to tell what this path/route function does
path function is nothing but a url/endpoint for the api

- we use python dict to send json as response

- async is to make an asynchronous call

Note: Here fastapi behaves in sequential manner
example - if you have two similar api endpoints the first match will be called
so the order matters
"""

"""
CRUD - Create Read Update Delete

there should be a meaningful name for the endpoint

Create - post       - /posts
Read   - get        - /posts or /posts/{id}
Update - put/patch  - /posts/{id}
Delete - delete     - /posts/{id}

"""

# py-dantic model to validate the schema


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional field with default value to be true
    rating: int | None = None  # optional field with default value to be none


my_posts = [{"title": "title 1", "content": "content 1", "published": True, "rating": 4, "id": 1}]


# function to find one post based on the id logic will change when we use database
def find_one(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# function to find the index of the post based on the id
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/api/v1/posts")
async def get_posts():
    return {"data": my_posts}


@app.get("/api/v1/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_one(id)
    if post:
        return {"data": post}
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": "failure", "message": "data  not found"}
        # we can also use above method and below line is another way of doing it
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")


# In below function since we don't have any else operation so we can also use this method to set the status code
# this is a default status code
@app.post("/api/v1/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}


"""
PUT   - put call is used to update the data in database/storage 
but while sending the payload we need to send the whole data with the parameter that needs to be updated

for example if we are updating title for post with id 1
the payload will be like 

{
    "title":"updated name", - name to be updated
    "content":"sample content" - original content
}

PATCH - patch call is also used to updated the data in database/storage
but here the trade secret is while sending the payload we just need to send the data that needs to updated

for example if we are updating title for post with id 1
the payload will be like 

{
    "title":"updated name", - name to be updated
}

"""


@app.put("/api/v1/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id  # setting the id because the payload comes from req doesn't have id
    my_posts[index] = post_dict
    return {"status": "success", "data": post_dict}


@app.delete("/api/v1/posts/{id}")
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
