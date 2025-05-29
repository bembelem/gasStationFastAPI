from sqlalchemy.orm import Session
from src.models.models import Customer
from src.schemas.customers import CustomerCreate, CustomerUpdate


def get_all_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_phone(db: Session, phone_number: str):
    return db.query(Customer).filter(Customer.phone_number == phone_number).first()


def create_customer(db: Session, customer_data: CustomerCreate):
    new_customer = Customer(**customer_data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def update_customer(db: Session, customer_id: int, customer_data: CustomerUpdate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    for field, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer_bonus_points(db: Session, customer_id: int, bonus_points: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    customer.bonus_points = bonus_points
    db.commit()
    db.refresh(customer)
    return customer


def update_customer_tier(db: Session, customer_id: int, tier_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    customer.client_tier_id = tier_id
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    db.delete(customer)
    db.commit()
    return customer
