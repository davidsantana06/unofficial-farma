from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[int] = None
    company_id: int
    name: str
    description: str
    price: float
    dosage: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
