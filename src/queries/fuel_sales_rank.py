from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import label
from sqlalchemy import select
from sqlalchemy import literal_column
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from sqlalchemy import over
from src.models.models import Station, StationTank, FuelType, RefuelingSession, SaleTransaction

def get_fuel_sales_rank(db: Session):
    subquery = (
        db.query(
            Station.name.label("station_name"),
            FuelType.name.label("fuel_name"),
            func.sum(SaleTransaction.total_amount).label("sales")
        )
        .join(StationTank, Station.id == StationTank.station_id)
        .join(FuelType, StationTank.fuel_type_id == FuelType.id)
        .join(RefuelingSession, FuelType.id == RefuelingSession.fuel_type_id)
        .join(SaleTransaction, RefuelingSession.sale_transaction_id == SaleTransaction.id)
        .filter(
            RefuelingSession.status_id == 3,
            SaleTransaction.status_id == 3
        )
        .group_by(Station.name, FuelType.name)
        .subquery()
    )

    query = (
        db.query(
            subquery.c.station_name,
            subquery.c.fuel_name,
            subquery.c.sales,
            over(
                func.rank(),
                partition_by=subquery.c.station_name,
                order_by=desc(subquery.c.sales)
            ).label("fuel_sales_rank")
        )
        .order_by(subquery.c.station_name, "fuel_sales_rank")
    )

    return query.all()
