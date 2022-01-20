from numbers import Real
from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time

app = FastAPI()

# SCHEMAS
# title: str, content: str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


f = open("config.json")
connection_data = json.load(f)
f.close()
while True:
    try:
        conn = psycopg2.connect(
            host=connection_data["host"],
            database=connection_data["database"],
            user=connection_data["user"],
            password=connection_data["password"],
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DATABASE CONNECTION SUCCESSFUL")
        break
    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(str(error))
        time.sleep(1)

myposts = [
    {"id": 1, "title": "Post 1", "content": "content 1"},
    {"id": 2, "title": "Post 2", "content": "content 2"},
]


def find_post(id: int):
    for p in myposts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(myposts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to first API"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALS (%s,%s,%s)
                   RETURNING *""",
        (post.title, post.content, post.published),
    )

    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = myposts[len(myposts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Find the index in the array that has the required ID
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    myposts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    myposts[index] = post_dict
    return {"data": post_dict}
