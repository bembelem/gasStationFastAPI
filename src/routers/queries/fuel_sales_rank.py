from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from src.queries.fuel_sales_rank import get_fuel_sales_rank
from src.schemas.queries.fuel_sales_rank import FuelSalesRank

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/fuel-sales-rank", response_model=list[FuelSalesRank])
def read_fuel_sales_rank(db: Session = Depends(get_db)):
    return get_fuel_sales_rank(db)
