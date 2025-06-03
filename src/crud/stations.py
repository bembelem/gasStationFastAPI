from sqlalchemy.orm import Session
from src.models.models import Station
from src.schemas.stations import StationCreate, StationUpdate
from fastapi import HTTPException

def get_all_stations(db: Session):
    return db.query(Station).all()


def get_station_by_id(db: Session, station_id: int):
    return db.query(Station).filter(Station.id == station_id).first()


def create_station(db: Session, station_data: StationCreate):
    station = Station(**station_data.dict())
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


def update_station(db: Session, station_id: int, station_data: StationUpdate):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        return None
    for key, value in station_data.model_dump(exclude_unset=True).items():
        setattr(station, key, value)
    db.commit()
    db.refresh(station)
    return station


def delete_station(db: Session, station_id: int):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        return None
    db.delete(station)
    db.commit()
    return station

def check_station_exists(db: Session, station_id: int):
    customer = db.query(Station).filter(station_id == Station.id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Станция не найдена")
    return customer