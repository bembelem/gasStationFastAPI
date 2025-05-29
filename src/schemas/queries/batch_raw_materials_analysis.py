from pydantic import BaseModel
from typing import Optional

class BatchRawMaterialsAnalysis(BaseModel):
    name: str
    expected_output_volume: float
    quality_check_passed: Optional[bool]
    way: str

    class Config:
        orm_mode = True