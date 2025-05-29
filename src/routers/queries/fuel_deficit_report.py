from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db  # или src.database.get_db, если нужен полный путь
from src.queries.fuel_deficit_report import get_fuel_deficit_report
from src.schemas.queries.fuel_deficit_report import FuelDeficitResponse

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/fuel-deficit", response_model=list[FuelDeficitResponse])
def read_fuel_deficit_report(db: Session = Depends(get_db)):
    return get_fuel_deficit_report(db)
