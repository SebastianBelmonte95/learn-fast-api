from .database import Base
from sqlalchemy import Column, Integer, Boolean, String


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=False, nullable=False)
    content = Column(String, primary_key=False, nullable=False)
    published = Column(Boolean, primary_key=False, nullable=False, default=True)
