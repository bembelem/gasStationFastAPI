from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from src.services.fuel_purchase_service import FuelPurchaseService
from src.schemas.fuel_purchase import FuelPurchaseRequest, FuelPurchaseResponse

router = APIRouter(
    prefix="/api/fuel-purchase",
    tags=["Services"]
)


@router.post("/", response_model=FuelPurchaseResponse)
def process_fuel_purchase(
        request: FuelPurchaseRequest,
        db: Session = Depends(get_db)
):

    service = FuelPurchaseService(db)

    return service.process_fuel_purchase(
        station_id=request.station_id,
        fuel_type_id=request.fuel_type_id,
        fuel_pump_id=request.fuel_pump_id,
        volume=request.volume,
        total_amount=request.total_amount,
        customer_id=request.customer_id,
        operator_id=request.operator_id,
        payment_method_id=request.payment_method_id,
        bonus_used=request.bonus_used
    )