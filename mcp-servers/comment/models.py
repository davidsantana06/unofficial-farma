from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Comment(BaseModel):
    id: Optional[int] = None
    product_id: int
    author_name: str
    author_email: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
