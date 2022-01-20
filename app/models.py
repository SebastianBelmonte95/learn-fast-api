from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, Boolean, String
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
