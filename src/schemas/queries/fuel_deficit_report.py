from pydantic import BaseModel
from typing import Optional

class FuelDeficitResponse(BaseModel):
    fuel_type: str
    supply_volume_requested: Optional[float] = 0
    production_volume_requested: Optional[float] = 0
    deficit_percentage: Optional[float] = 0

    class Config:
        orm_mode = True
