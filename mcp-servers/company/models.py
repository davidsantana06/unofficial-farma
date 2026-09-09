from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Company(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
