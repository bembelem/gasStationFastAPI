from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.models import SupplyOrder, Station, StationTank, ProductionOrder, FuelType

def get_fuel_deficit_report(db: Session):
    # объём, который нужно восполнить по заявкам на поставку
    supply_subquery = (
        db.query(
            SupplyOrder.fuel_type_id.label("fuel_type_id"),
            func.sum(StationTank.capacity - StationTank.current_volume).label("supply_volume_requested")
        )
        .join(Station, SupplyOrder.station_id == Station.id)
        .join(StationTank, Station.id == StationTank.station_id)
        .filter(SupplyOrder.status_id != 5)
        .group_by(SupplyOrder.fuel_type_id)
        .subquery()
    )

    # объём, заказанный на производство
    production_subquery = (
        db.query(
            ProductionOrder.fuel_type_id.label("fuel_type_id"),
            func.sum(ProductionOrder.volume_requested).label("production_volume_requested")
        )
        .filter(ProductionOrder.status_id != 5)
        .group_by(ProductionOrder.fuel_type_id)
        .subquery()
    )

    query = (
        db.query(
            FuelType.name.label("fuel_type"),
            supply_subquery.c.supply_volume_requested,
            production_subquery.c.production_volume_requested,
            (production_subquery.c.production_volume_requested / supply_subquery.c.supply_volume_requested * 100)
            .label("deficit_percentage")
        )
        .join(supply_subquery, FuelType.id == supply_subquery.c.fuel_type_id)
        .join(production_subquery, FuelType.id == production_subquery.c.fuel_type_id)
    )

    return query.all()
