from cgi import test
from numbers import Real
from os import stat
from sqlite3 import dbapi2
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time
from . import models
from models import Post
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Staged changes
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    # Commiting change to DB
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = myposts[len(myposts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *;""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"post_detail": updated_post}
