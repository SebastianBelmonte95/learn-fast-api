from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time
from . import models
from .models import Post
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    print(posts)
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase
)
def create_post(post: schemas.PostCreate):
    # Staged changes
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    # Commiting change to DB
    conn.commit()
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    post = myposts[len(myposts) - 1]
    return post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return post


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
def update_post(id: int, post: schemas.PostCreate, response_model=schemas.PostBase):
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
    return updated_post
