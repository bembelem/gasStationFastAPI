from sqlalchemy.orm import Session
from src.models.models import Refinery
from src.schemas.refineries import RefineryCreate, RefineryUpdate
from fastapi import HTTPException

def get_all_refineries(db: Session):
    return db.query(Refinery).all()

def get_refinery_by_id(db: Session, refinery_id: int):
    return check_refinery_exists(db, refinery_id)

def create_refinery(db: Session, refinery_data: RefineryCreate):
    new_refinery = Refinery(**refinery_data.model_dump())
    db.add(new_refinery)
    db.commit()
    db.refresh(new_refinery)
    return new_refinery

def update_refinery(db: Session, refinery_id: int, refinery_data: RefineryUpdate):
    refinery = check_refinery_exists(db, refinery_id)
    for field, value in refinery_data.model_dump(exclude_unset=True).items():
        setattr(refinery, field, value)
    db.commit()
    db.refresh(refinery)
    return refinery

def delete_refinery(db: Session, refinery_id: int):
    refinery = check_refinery_exists(db, refinery_id)
    db.delete(refinery)
    db.commit()
    return refinery

def check_refinery_exists(db: Session, refinery_id: int):
    refinery = db.query(Refinery).filter(Refinery.id == refinery_id).first()
    if not refinery:
        raise HTTPException(status_code=404, detail="НПЗ не найден")
    return refinery
