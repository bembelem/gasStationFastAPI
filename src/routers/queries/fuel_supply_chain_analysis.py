from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from src.queries.fuel_supply_chain_analysis import (
    get_fuel_supply_chain_analysis
)
from src.schemas.queries.fuel_supply_chain_analysis import FuelSupplyChainAnalysis

router = APIRouter(
    prefix="/api",
    tags=["Queries"]
)


@router.get("/fuel-supply-chain", response_model=List[FuelSupplyChainAnalysis])
def read_fuel_supply_chain_analysis(
        use_orm: bool = Query(False, description="Use ORM-based recursive implementation"),
        db: Session = Depends(get_db)
):
    if use_orm:
        return get_fuel_supply_chain_analysis(db)
    else:
        results = get_fuel_supply_chain_analysis(db)
        return [
            FuelSupplyChainAnalysis(
                id=row[0],
                name=row[1],
                address=row[2],
                contact_number=row[3],
                way=row[4]
            ) for row in results
        ]