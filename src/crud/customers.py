from sqlalchemy.orm import Session
from src.models.models import Customer
from src.schemas.customers import CustomerCreate, CustomerUpdate
from fastapi import HTTPException

def get_all_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return check_customer_exists(db, customer_id)

def create_customer(db: Session, customer_data: CustomerCreate):
    check_phone_not_taken(db, customer_data.phone_number)
    new_customer = Customer(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def update_customer(db: Session, customer_id: int, customer_data: CustomerUpdate):
    customer = check_customer_exists(db, customer_id)
    for field, value in customer_data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer

def update_customer_bonus_points(db: Session, customer_id: int, bonus_points: int):
    customer = check_customer_exists(db, customer_id)
    customer.bonus_points = bonus_points
    db.commit()
    db.refresh(customer)
    return customer

def update_customer_tier(db: Session, customer_id: int, tier_id: int):
    customer = check_customer_exists(db, customer_id)
    customer.client_tier_id = tier_id
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = check_customer_exists(db, customer_id)
    db.delete(customer)
    db.commit()
    return customer

def check_customer_exists(db: Session, customer_id: int):
    customer = db.query(Customer).filter(customer_id == Customer.id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return customer

def check_phone_not_taken(db: Session, phone_number: str):
    exists = db.query(Customer).filter(phone_number == Customer.phone_number).first()
    if exists:
        raise HTTPException(status_code=400, detail="Телефон уже зарегистрирован")