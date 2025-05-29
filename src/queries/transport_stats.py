from sqlalchemy.orm import Session
from sqlalchemy import func, case, literal, cast
from sqlalchemy.sql import label
from datetime import datetime, timedelta
from src.models.models import Transport, TransportStatus, TransferTransport, FuelTransfer, TransferStatus

def get_transport_stats(db: Session):
    # для ID незавершённых статусов
    incomplete_status_ids = (
        db.query(TransferStatus.id)
        .filter(TransferStatus.name.like("In Transit%") | (TransferStatus.name == "Scheduled"))
        .subquery()
    )

    thirty_days_ago = datetime.now() - timedelta(days=30)

    query = (
        db.query(
            Transport.transport_number.label("transport_number"),
            Transport.transport_type.label("transport_type"),
            TransportStatus.name.label("status"),
            func.count(FuelTransfer.id).label("transfer_count"),
            func.sum(TransferTransport.volume).label("total_volume_transferred"),
            Transport.capacity.label("capacity"),
            (func.avg(
                (func.julianday(FuelTransfer.received_at) - func.julianday(FuelTransfer.dispatched_at)) * 24
            )).label("avg_delivery_time_hours"),
            func.sum(
                case(
                    (FuelTransfer.status_id.in_(incomplete_status_ids), 1),
                    else_=0
                )
            ).label("incomplete_transfers"),
            Transport.current_location.label("current_location")
        )
        .join(TransportStatus, Transport.status == TransportStatus.id)
        .outerjoin(TransferTransport, Transport.id == TransferTransport.transport_id)
        .outerjoin(FuelTransfer, TransferTransport.transfer_id == FuelTransfer.id)
        .filter(FuelTransfer.dispatched_at >= thirty_days_ago)
        .group_by(Transport.id)
        .order_by(func.count(FuelTransfer.id).desc())
    )

    return query.all()
