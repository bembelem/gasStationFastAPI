from sqlalchemy.orm import Session
from src.models.models import StationTank
from src.schemas.station_tanks import StationTankCreate, StationTankUpdate, StationTankVolumeUpdate
from fastapi import HTTPException

def get_all_station_tanks(db: Session):
    return db.query(StationTank).all()

def get_station_tank_by_id(db: Session, tank_id: int):
    return db.query(StationTank).filter(StationTank.id == tank_id).first()

def get_station_tanks_by_station_id(db: Session, station_id: int):
    return db.query(StationTank).filter(StationTank.station_id == station_id).all()

def create_station_tank(db: Session, tank_data: StationTankCreate):
    new_tank = StationTank(**tank_data.dict())
    db.add(new_tank)
    db.commit()
    db.refresh(new_tank)
    return new_tank

def update_station_tank(db: Session, tank_id: int, tank_data: StationTankUpdate):
    tank = check_tank_exists(db, tank_id)
    for field, value in tank_data.model_dump(exclude_unset=True).items():
        setattr(tank, field, value)
    db.commit()
    db.refresh(tank)
    return tank

def update_station_tank_volume(db: Session, tank_id: int, volume_data: StationTankVolumeUpdate):
    tank = check_tank_exists(db, tank_id)
    check_volume_within_limit(tank, volume_data.current_volume)
    tank.current_volume = volume_data.current_volume
    db.commit()
    db.refresh(tank)
    return tank

def delete_station_tank(db: Session, tank_id: int):
    tank = get_station_tank_by_id(db, tank_id)
    if not tank:
        return None
    db.delete(tank)
    db.commit()
    return tank

def check_tank_exists(db: Session, tank_id: int):
    tank = db.query(StationTank).filter(StationTank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Резервуар не найден")
    return tank

def check_volume_within_limit(tank: StationTank, new_volume: float):
    if new_volume > tank.capacity:
        raise HTTPException(status_code=400, detail="Новый объём превышает вместимость резервуара")
