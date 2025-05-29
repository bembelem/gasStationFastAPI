from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from src.queries.hourly_sales_report import get_sales_by_hour
from src.schemas.queries.hourly_sales_report import HourlySalesResponse

router = APIRouter(prefix="/api/query", tags=["Queries"])

@router.get("/hourly-sales", response_model=List[HourlySalesResponse])
def hourly_sales_report(db: Session = Depends(get_db)):
    return get_sales_by_hour(db)
