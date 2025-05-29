from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class FuelTypeBase(BaseModel):
    name: str = Field(..., description="Название типа топлива")
    price_per_unit: float = Field(..., gt=0, description="Цена за единицу")


class FuelTypeCreate(FuelTypeBase):
    pass


class FuelTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название типа топлива")
    price_per_unit: Optional[float] = Field(None, gt=0, description="Цена за единицу")


class FuelTypeResponse(FuelTypeBase):
    id: int

    class Config:
        from_attributes = True