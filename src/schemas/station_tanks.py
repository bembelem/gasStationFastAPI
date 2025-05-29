from pydantic import BaseModel, Field
from typing import Optional


class StationTankBase(BaseModel):
    station_id: int = Field(..., description="ID АЗС")
    fuel_type_id: int = Field(..., description="ID типа топлива")
    capacity: float = Field(..., gt=0, description="Вместимость резервуара")
    current_volume: float = Field(..., ge=0, description="Текущий объём")


class StationTankCreate(StationTankBase):
    pass


class StationTankUpdate(BaseModel):
    station_id: Optional[int]
    fuel_type_id: Optional[int]
    capacity: Optional[float] = Field(None, gt=0)
    current_volume: Optional[float] = Field(None, ge=0)


class StationTankVolumeUpdate(BaseModel):
    current_volume: float = Field(..., ge=0, description="Новый объём")


class StationTankResponse(StationTankBase):
    id: int

    class Config:
        from_attributes = True
