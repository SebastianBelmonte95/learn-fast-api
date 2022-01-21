from .database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=False, nullable=False)
    content = Column(String, primary_key=False, nullable=False)
    published = Column(
        Boolean, primary_key=False, nullable=False, server_default="TRUE"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, primary_key=False, nullable=False)
