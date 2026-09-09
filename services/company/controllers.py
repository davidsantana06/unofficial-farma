from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Company
from schemas import CompanyCreate, CompanyUpdate

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "company"}


@router.post("/companies", response_model=Company, status_code=201)
def create_company(payload: CompanyCreate, session: Session = Depends(get_session)):
    company = Company.model_validate(payload)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


@router.get("/companies", response_model=list[Company])
def list_companies(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    return session.exec(select(Company).offset(offset).limit(limit)).all()


@router.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="company not found")
    return company


@router.patch("/companies/{company_id}", response_model=Company)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    session: Session = Depends(get_session),
):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="company not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(company, key, value)
    company.updated_at = datetime.now(timezone.utc)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


@router.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: int, session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="company not found")
    session.delete(company)
    session.commit()
