from sqlalchemy.orm import Session
from src.models.models import RefineryTank
from src.schemas.refinery_tanks import RefineryTankCreate, RefineryTankUpdate, VolumeUpdate

def get_all_tanks(db: Session):
    return db.query(RefineryTank).all()

def get_tank_by_id(db: Session, tank_id: int):
    return db.query(RefineryTank).filter(RefineryTank.id == tank_id).first()

def get_tanks_by_refinery(db: Session, refinery_id: int):
    return db.query(RefineryTank).filter(RefineryTank.refinery_id == refinery_id).all()

def create_tank(db: Session, tank_data: RefineryTankCreate):
    tank = RefineryTank(**tank_data.dict())
    db.add(tank)
    db.commit()
    db.refresh(tank)
    return tank

def update_tank(db: Session, tank_id: int, tank_data: RefineryTankUpdate):
    tank = db.query(RefineryTank).filter(RefineryTank.id == tank_id).first()
    if not tank:
        return None
    for field, value in tank_data.dict(exclude_unset=True).items():
        setattr(tank, field, value)
    db.commit()
    db.refresh(tank)
    return tank

def update_volume(db: Session, tank_id: int, volume_data: VolumeUpdate):
    tank = db.query(RefineryTank).filter(RefineryTank.id == tank_id).first()
    if not tank:
        return None
    tank.current_volume = volume_data.current_volume
    db.commit()
    db.refresh(tank)
    return tank

def delete_tank(db: Session, tank_id: int):
    tank = db.query(RefineryTank).filter(RefineryTank.id == tank_id).first()
    if not tank:
        return None
    db.delete(tank)
    db.commit()
    return tank
