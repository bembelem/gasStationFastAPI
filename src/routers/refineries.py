from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.crud import refineries as crud
from src.schemas.refineries import RefineryResponse, RefineryCreate, RefineryUpdate
from database import get_db

router = APIRouter(
    prefix="/api/refineries",
    tags=["Refineries"]
)

@router.get("/", response_model=List[RefineryResponse])
def read_all_refineries(db: Session = Depends(get_db)):
    return crud.get_all_refineries(db)

@router.get("/{refinery_id}", response_model=RefineryResponse)
def read_refinery(refinery_id: int, db: Session = Depends(get_db)):
    refinery = crud.get_refinery_by_id(db, refinery_id)
    if not refinery:
        raise HTTPException(status_code=404, detail="Refinery not found")
    return refinery

@router.post("/", response_model=RefineryResponse, status_code=201)
def create_refinery(refinery_data: RefineryCreate, db: Session = Depends(get_db)):
    return crud.create_refinery(db, refinery_data)

@router.put("/{refinery_id}", response_model=RefineryResponse)
def update_refinery(refinery_id: int, refinery_data: RefineryUpdate, db: Session = Depends(get_db)):
    refinery = crud.update_refinery(db, refinery_id, refinery_data)
    if not refinery:
        raise HTTPException(status_code=404, detail="Refinery not found")
    return refinery

@router.delete("/{refinery_id}", response_model=RefineryResponse)
def delete_refinery(refinery_id: int, db: Session = Depends(get_db)):
    refinery = crud.delete_refinery(db, refinery_id)
    if not refinery:
        raise HTTPException(status_code=404, detail="Refinery not found")
    return refinery
