from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.crud import station_tanks as crud
from src.schemas.station_tanks import (
    StationTankResponse, StationTankCreate, StationTankUpdate, StationTankVolumeUpdate
)
from database import get_db

router = APIRouter(
    prefix="/api/station-tanks",
    tags=["Station Tanks"]
)

@router.get("/", response_model=List[StationTankResponse])
def read_all_tanks(db: Session = Depends(get_db)):
    return crud.get_all_station_tanks(db)

@router.get("/{tank_id}", response_model=StationTankResponse)
def read_tank_by_id(tank_id: int, db: Session = Depends(get_db)):
    tank = crud.get_station_tank_by_id(db, tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Station tank not found")
    return tank

@router.get("/station/{station_id}", response_model=List[StationTankResponse])
def read_tanks_by_station(station_id: int, db: Session = Depends(get_db)):
    return crud.get_station_tanks_by_station_id(db, station_id)

@router.post("/", response_model=StationTankResponse, status_code=201)
def create_tank(tank_data: StationTankCreate, db: Session = Depends(get_db)):
    return crud.create_station_tank(db, tank_data)

@router.put("/{tank_id}", response_model=StationTankResponse)
def update_tank(tank_id: int, tank_data: StationTankUpdate, db: Session = Depends(get_db)):
    tank = crud.update_station_tank(db, tank_id, tank_data)
    if not tank:
        raise HTTPException(status_code=404, detail="Station tank not found")
    return tank

@router.patch("/{tank_id}/volume", response_model=StationTankResponse)
def update_volume(tank_id: int, volume_data: StationTankVolumeUpdate, db: Session = Depends(get_db)):
    tank = crud.update_station_tank_volume(db, tank_id, volume_data)
    if not tank:
        raise HTTPException(status_code=404, detail="Station tank not found")
    return tank

@router.delete("/{tank_id}", response_model=StationTankResponse)
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    tank = crud.delete_station_tank(db, tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Station tank not found")
    return tank
