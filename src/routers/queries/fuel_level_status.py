from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from src.schemas.queries.fuel_level_status import FuelLevelResponse
from src.queries.fuel_level_status import get_critical_fuel_levels

router = APIRouter(prefix="/api/query", tags=["Queries"])

@router.get("/low-fuel", response_model=list[FuelLevelResponse])
def get_low_fuel_stations(db: Session = Depends(get_db)):
    rows = get_critical_fuel_levels(db)
    return [FuelLevelResponse(**dict(row._mapping)) for row in rows]
