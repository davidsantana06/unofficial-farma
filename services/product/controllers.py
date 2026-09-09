from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import httpx

from database import get_session
from models import Product
from schemas import ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "product"}


@router.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate, session: Session = Depends(get_session)):
    response = httpx.get(
        f"http://unofficial-farma-company-service:8001/companies/{payload.company_id}"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="company not found")
    product = Product.model_validate(payload)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.get("/products", response_model=list[Product])
def list_products(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    return session.exec(select(Product).offset(offset).limit(limit)).all()


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@router.patch("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    data = payload.model_dump(exclude_unset=True)
    if "company_id" in data:
        company_id = data["company_id"]
        response = httpx.get(
            f"http://unofficial-farma-company-service:8001/companies/{company_id}"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="company not found")
    for key, value in data.items():
        setattr(product, key, value)
    product.updated_at = datetime.now(timezone.utc)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    session.delete(product)
    session.commit()
