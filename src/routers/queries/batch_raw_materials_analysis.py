from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from src.queries.batch_raw_materials_analysis import get_batch_raw_materials_analysis
from src.schemas.queries.batch_raw_materials_analysis import BatchRawMaterialsAnalysis

router = APIRouter(
    prefix="/api",
    tags=["Queries"]
)

@router.get("/batch-raw-materials-analysis", response_model=List[BatchRawMaterialsAnalysis])
def read_batch_raw_materials_analysis(db: Session = Depends(get_db)):
    return get_batch_raw_materials_analysis(db)
