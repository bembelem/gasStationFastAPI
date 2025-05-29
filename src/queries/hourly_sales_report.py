from sqlalchemy.orm import Session
from sqlalchemy import func, extract, cast, Integer
from src.models.models import (
    SaleTransaction, RefuelingSession, FuelType,
    FuelPump, FuelDispenser, Station
)

def get_sales_by_hour(db: Session):
    hour_of_day = func.strftime('%H', SaleTransaction.transaction_date_time).label("hour_of_day")

    query = (
        db.query(
            Station.name.label("station"),
            FuelType.name.label("fuel_type"),
            hour_of_day,
            func.count().label("transaction_count"),
            func.round(func.sum(SaleTransaction.volume), 2).label("total_volume"),
            func.round(func.sum(SaleTransaction.total_amount), 2).label("total_amount"),
            func.round(func.avg(SaleTransaction.total_amount), 2).label("average_receipt"),
            func.round(func.sum(SaleTransaction.volume) / func.count(), 2).label("average_volume_per_transaction")
        )
        .join(RefuelingSession, SaleTransaction.id == RefuelingSession.sale_transaction_id)
        .join(FuelType, RefuelingSession.fuel_type_id == FuelType.id)
        .join(FuelPump, RefuelingSession.fuel_pump_id == FuelPump.id)
        .join(FuelDispenser, FuelPump.fuel_dispenser_id == FuelDispenser.id)
        .join(Station, FuelDispenser.station_id == Station.id)
        .filter(SaleTransaction.status_id == 3)
        .filter(SaleTransaction.transaction_date_time >= func.date("now", "-6 months"))
        .group_by(Station.name, FuelType.name, hour_of_day)
        .order_by(Station.name, FuelType.name, hour_of_day)
    )

    return query.all()
