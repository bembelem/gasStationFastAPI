from sqlalchemy.orm import Session
from src.models.models import FuelType
from src.schemas.fuel_types import FuelTypeCreate, FuelTypeUpdate

# Получить все записи
def get_all_fuel_types(db: Session):
    return db.query(FuelType).all()

def get_fuel_by_id(db: Session, fuel_type_id: int):
    return db.query(FuelType).filter(fuel_type_id == FuelType.id).first()

def create_fuel_type(db: Session, fuel_type_data: FuelTypeCreate):
    new_fuel_type = FuelType(**fuel_type_data.dict())
    db.add(new_fuel_type)
    db.commit()
    db.refresh(new_fuel_type)
    return new_fuel_type

def update_fuel_type(db: Session, fuel_type_id: int,  fuel_type_data: FuelTypeUpdate):
    fuel_type = db.query(FuelType).filter(fuel_type_id == FuelType.id).first()
    if not fuel_type: return None
    for field, value in fuel_type_data.dict(exclude_unset=True).items():
        setattr(fuel_type, field, value)
    db.commit()
    db.refresh(fuel_type)
    return fuel_type

def delete_fuel_type(db: Session, fuel_type_id: int):
    fuel_type = db.query(FuelType).filter(fuel_type_id == FuelType.id).first()
    if not fuel_type:
        return None
    db.delete(fuel_type)
    db.commit()
    return fuel_type
