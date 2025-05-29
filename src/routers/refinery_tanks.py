from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.schemas.refinery_tanks import (
    RefineryTankResponse, RefineryTankCreate, RefineryTankUpdate, VolumeUpdate
)
from src.crud import refinery_tanks as crud
from database import get_db

router = APIRouter(
    prefix="/api/refinery-tanks",
    tags=["Refinery Tanks"]
)

@router.get("/", response_model=List[RefineryTankResponse])
def read_all_tanks(db: Session = Depends(get_db)):
    return crud.get_all_tanks(db)

@router.get("/{tank_id}", response_model=RefineryTankResponse)
def read_tank_by_id(tank_id: int, db: Session = Depends(get_db)):
    tank = crud.get_tank_by_id(db, tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank

@router.get("/refinery/{refinery_id}/tanks", response_model=List[RefineryTankResponse])
def read_tanks_by_refinery(refinery_id: int, db: Session = Depends(get_db)):
    return crud.get_tanks_by_refinery(db, refinery_id)

@router.post("/", response_model=RefineryTankResponse, status_code=201)
def create_tank(tank_data: RefineryTankCreate, db: Session = Depends(get_db)):
    return crud.create_tank(db, tank_data)

@router.put("/{tank_id}", response_model=RefineryTankResponse)
def update_tank(tank_id: int, tank_data: RefineryTankUpdate, db: Session = Depends(get_db)):
    tank = crud.update_tank(db, tank_id, tank_data)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank

@router.patch("/{tank_id}/volume", response_model=RefineryTankResponse)
def update_tank_volume(tank_id: int, volume_data: VolumeUpdate, db: Session = Depends(get_db)):
    tank = crud.update_volume(db, tank_id, volume_data)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank

@router.delete("/{tank_id}", response_model=RefineryTankResponse)
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    tank = crud.delete_tank(db, tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank
