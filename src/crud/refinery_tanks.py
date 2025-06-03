from sqlalchemy.orm import Session
from src.models.models import RefineryTank
from src.schemas.refinery_tanks import RefineryTankCreate, RefineryTankUpdate, VolumeUpdate
from fastapi import HTTPException

def get_all_tanks(db: Session):
    return db.query(RefineryTank).all()

def get_tank_by_id(db: Session, tank_id: int):
    return check_tank_exists(db, tank_id)

def get_tanks_by_refinery(db: Session, refinery_id: int):
    return db.query(RefineryTank).filter(refinery_id == RefineryTank.refinery_id).all()

def create_tank(db: Session, tank_data: RefineryTankCreate):
    tank = RefineryTank(**tank_data.model_dump())
    db.add(tank)
    db.commit()
    db.refresh(tank)
    return tank

def update_tank(db: Session, tank_id: int, tank_data: RefineryTankUpdate):
    tank = check_tank_exists(db, tank_id)
    for field, value in tank_data.model_dump(exclude_unset=True).items():
        setattr(tank, field, value)
    db.commit()
    db.refresh(tank)
    return tank

def update_volume(db: Session, tank_id: int, volume_data: VolumeUpdate):
    tank = check_tank_exists(db, tank_id)
    check_volume_within_limit(tank, volume_data.current_volume)
    tank.current_volume = volume_data.current_volume
    db.commit()
    db.refresh(tank)
    return tank

def delete_tank(db: Session, tank_id: int):
    tank = check_tank_exists(db, tank_id)
    db.delete(tank)
    db.commit()
    return tank

def check_tank_exists(db: Session, tank_id: int):
    tank = db.query(RefineryTank).filter(RefineryTank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Резервуар не найден")
    return tank

def check_volume_within_limit(tank: RefineryTank, new_volume: float):
    if new_volume > tank.capacity:
        raise HTTPException(status_code=400, detail="Новый объём превышает вместимость резервуара")
