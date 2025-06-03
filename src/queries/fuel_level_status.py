from sqlalchemy.orm import Session
from sqlalchemy import case
from src.models.models import StationTank, Station, FuelType

def get_critical_fuel_levels(db: Session):
    percentage = (StationTank.current_volume / StationTank.capacity * 100).label("fill_percentage")
    stock_status = case(
        (
            ((StationTank.current_volume / StationTank.capacity * 100) < 15), "Критический"
        ),
        (
            ((StationTank.current_volume / StationTank.capacity * 100) < 30), "Низкий"
        ),
        else_="Нормальный"
    ).label("stock_status")

    query = (
        db.query(
            Station.name.label("station"),
            Station.address.label("address"),
            FuelType.name.label("fuel_type"),
            StationTank.current_volume,
            StationTank.capacity,
            percentage,
            stock_status
        )
        .select_from(StationTank)
        .join(StationTank.station)
        .join(StationTank.fuel_type)
        .filter(percentage < 30)
        .order_by(percentage)
    )

    return query.all()
