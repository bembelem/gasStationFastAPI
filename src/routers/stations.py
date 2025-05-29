from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.schemas.stations import StationResponse, StationCreate, StationUpdate
from src.crud import stations as crud
from database import get_db

router = APIRouter(
    prefix="/api/stations",
    tags=["Stations"]
)

@router.get("/", response_model=List[StationResponse])
def read_all_stations(db: Session = Depends(get_db)):
    return crud.get_all_stations(db)

@router.get("/{station_id}", response_model=StationResponse)
def read_station_by_id(station_id: int, db: Session = Depends(get_db)):
    station = crud.get_station_by_id(db, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@router.post("/", response_model=StationResponse, status_code=201)
def create_station(station_data: StationCreate, db: Session = Depends(get_db)):
    return crud.create_station(db, station_data)

@router.put("/{station_id}", response_model=StationResponse)
def update_station(station_id: int, station_data: StationUpdate, db: Session = Depends(get_db)):
    station = crud.update_station(db, station_id, station_data)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@router.delete("/{station_id}", response_model=StationResponse)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    station = crud.delete_station(db, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station
