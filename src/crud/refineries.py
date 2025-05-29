from sqlalchemy.orm import Session
from src.models.models import Refinery
from src.schemas.refineries import RefineryCreate, RefineryUpdate

def get_all_refineries(db: Session):
    return db.query(Refinery).all()

def get_refinery_by_id(db: Session, refinery_id: int):
    return db.query(Refinery).filter(Refinery.id == refinery_id).first()

def create_refinery(db: Session, refinery_data: RefineryCreate):
    new_refinery = Refinery(**refinery_data.dict())
    db.add(new_refinery)
    db.commit()
    db.refresh(new_refinery)
    return new_refinery

def update_refinery(db: Session, refinery_id: int, refinery_data: RefineryUpdate):
    refinery = db.query(Refinery).filter(Refinery.id == refinery_id).first()
    if not refinery:
        return None
    for field, value in refinery_data.dict(exclude_unset=True).items():
        setattr(refinery, field, value)
    db.commit()
    db.refresh(refinery)
    return refinery

def delete_refinery(db: Session, refinery_id: int):
    refinery = db.query(Refinery).filter(Refinery.id == refinery_id).first()
    if not refinery:
        return None
    db.delete(refinery)
    db.commit()
    return refinery
