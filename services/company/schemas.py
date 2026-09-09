from sqlmodel import SQLModel
from typing import Optional


class CompanyBase(SQLModel):
    name: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(SQLModel):
    name: Optional[str] = None
