from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.crud import fuel_types as crud
from src.schemas.fuel_types import FuelTypeResponse, FuelTypeCreate, FuelTypeUpdate
from database import get_db

router = APIRouter(
    prefix="/api/fuel-types",
    tags=["Fuel Types"]
)

@router.get("/", response_model=List[FuelTypeResponse])
def read_all_fuel_types(db: Session = Depends(get_db)):
    return crud.get_all_fuel_types(db)

@router.get("/{fuel_type_id}", response_model=FuelTypeResponse)
def read_fuel_type(fuel_type_id: int, db: Session = Depends(get_db)):
    fuel_type = crud.get_fuel_by_id(db, fuel_type_id)
    if not fuel_type:
        raise HTTPException(status_code=404, detail="Fuel type not found")
    return fuel_type

@router.post("/", response_model=FuelTypeResponse, status_code=201)
def create_fuel_type(fuel_type_data: FuelTypeCreate, db: Session = Depends(get_db)):
    return crud.create_fuel_type(db, fuel_type_data)

@router.put("/{fuel_type_id}", response_model=FuelTypeResponse)
def update_fuel_type(fuel_type_id: int, fuel_type_data: FuelTypeUpdate, db: Session = Depends(get_db)):
    fuel_type = crud.update_fuel_type(db, fuel_type_id, fuel_type_data)
    if not fuel_type:
        raise HTTPException(status_code=404, detail="Fuel type not found")
    return fuel_type

@router.delete("/{fuel_type_id}", response_model=FuelTypeResponse)
def delete_fuel_type(fuel_type_id: int, db: Session = Depends(get_db)):
    fuel_type = crud.delete_fuel_type(db, fuel_type_id)
    if not fuel_type:
        raise HTTPException(status_code=404, detail="Fuel type not found")
    return fuel_type