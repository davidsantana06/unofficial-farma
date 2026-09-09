from sqlmodel import SQLModel
from typing import Optional


class ProductBase(SQLModel):
    company_id: int
    name: str
    description: str
    price: float
    dosage: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    company_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    dosage: Optional[str] = None
