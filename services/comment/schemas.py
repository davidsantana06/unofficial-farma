from sqlmodel import SQLModel
from typing import Optional


class CommentBase(SQLModel):
    product_id: int
    author_name: str
    author_email: str
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    product_id: Optional[int] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    content: Optional[str] = None


class CommentSearch(SQLModel):
    product_id: Optional[int] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    content: Optional[str] = None
