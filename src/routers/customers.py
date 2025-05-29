from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from src.schemas.customers import CustomerResponse, CustomerCreate, CustomerUpdate
from src.crud import customers as crud

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)

@router.get("/", response_model=List[CustomerResponse])
def read_all_customers(db: Session = Depends(get_db)):
    return crud.get_all_customers(db)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/phone/{phone_number}", response_model=CustomerResponse)
def read_customer_by_phone(phone_number: str, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_phone(db, phone_number)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer_data)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = crud.update_customer(db, customer_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.patch("/{customer_id}/bonus-points", response_model=CustomerResponse)
def update_bonus_points(customer_id: int, bonus_points: int, db: Session = Depends(get_db)):
    customer = crud.update_customer_bonus_points(db, customer_id, bonus_points)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.patch("/{customer_id}/tier", response_model=CustomerResponse)
def update_tier(customer_id: int, tier_id: int, db: Session = Depends(get_db)):
    customer = crud.update_customer_tier(db, customer_id, tier_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.delete_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
