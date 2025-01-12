# from pydantic import BaseModel
#
#
# class Post(BaseModel):
#     id: int
#     title: str
#     body: str


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    body = Column(String, unique=True, index=True, nullable=False)