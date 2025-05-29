from pydantic import BaseModel, Field
from typing import Optional


class RefineryTankBase(BaseModel):
    refinery_id: int
    fuel_type_id: int
    capacity: float = Field(..., gt=0)
    current_volume: float = Field(..., ge=0)


class RefineryTankCreate(RefineryTankBase):
    pass


class RefineryTankUpdate(BaseModel):
    refinery_id: Optional[int]
    fuel_type_id: Optional[int]
    capacity: Optional[float] = Field(None, gt=0)
    current_volume: Optional[float] = Field(None, ge=0)


class VolumeUpdate(BaseModel):
    current_volume: float = Field(..., ge=0)


class RefineryTankResponse(RefineryTankBase):
    id: int

    class Config:
        from_attributes = True
