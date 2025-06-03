from sqlalchemy.orm import Session
from src.models.models import FuelType
from src.schemas.fuel_types import FuelTypeCreate, FuelTypeUpdate
from fastapi import HTTPException

def get_all_fuel_types(db: Session):
    return db.query(FuelType).all()

def get_fuel_by_id(db: Session, fuel_type_id: int):
    return check_fuel_type_exists(db, fuel_type_id)

def create_fuel_type(db: Session, fuel_type_data: FuelTypeCreate):
    new_fuel_type = FuelType(**fuel_type_data.model_dump())
    db.add(new_fuel_type)
    db.commit()
    db.refresh(new_fuel_type)
    return new_fuel_type

def update_fuel_type(db: Session, fuel_type_id: int, fuel_type_data: FuelTypeUpdate):
    fuel_type = check_fuel_type_exists(db, fuel_type_id)
    for field, value in fuel_type_data.model_dump(exclude_unset=True).items():
        setattr(fuel_type, field, value)
    db.commit()
    db.refresh(fuel_type)
    return fuel_type

def delete_fuel_type(db: Session, fuel_type_id: int):
    fuel_type = check_fuel_type_exists(db, fuel_type_id)
    db.delete(fuel_type)
    db.commit()
    return fuel_type

def check_fuel_type_exists(db: Session, fuel_type_id: int):
    fuel_type = db.query(FuelType).filter(fuel_type_id == FuelType.id).first()
    if not fuel_type:
        raise HTTPException(status_code=404, detail="Тип топлива не найден")
    return fuel_type