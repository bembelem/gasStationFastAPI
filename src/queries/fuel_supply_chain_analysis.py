from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models.models import Station, FuelTransfer, RefineryTank, StationTank


def get_fuel_supply_chain_analysis(db: Session):
    # Начальные узлы (из НПЗ с ID=3)
    initial_transfers = (
        db.query(FuelTransfer)
        .join(RefineryTank, FuelTransfer.source_id == RefineryTank.id)
        .filter(
            FuelTransfer.status_id == 3,
            FuelTransfer.source_type_id == 1,
            RefineryTank.refinery_id == 3
        )
        .all()
    )

    def build_chain(transfer, path="", visited=None):
        if visited is None:
            visited = set()

        if transfer.id in visited:
            return []

        visited.add(transfer.id)
        current_path = f"{path} -> {transfer.id}" if path else str(transfer.id)
        chains = []

        # Если достигли станции (destination_type_id = 3)
        if transfer.destination_type_id == 3:
            station = (
                db.query(Station)
                .join(StationTank, Station.id == StationTank.station_id)
                .filter(StationTank.id == transfer.destination_id)
                .first()
            )
            if station:
                chains.append({
                    'id': station.id,
                    'name': station.name,
                    'address': station.address,
                    'contact_number': station.contact_number,
                    'way': current_path
                })

        # Поиск следующих трансферов
        next_transfers = (
            db.query(FuelTransfer)
            .filter(
                FuelTransfer.status_id == 3,
                FuelTransfer.source_id == transfer.destination_id,
                FuelTransfer.source_type_id == transfer.destination_type_id
            )
            .all()
        )

        for next_transfer in next_transfers:
            chains.extend(build_chain(next_transfer, current_path, visited.copy()))

        return chains

    all_chains = []
    for initial in initial_transfers:
        all_chains.extend(build_chain(initial))

    return all_chains