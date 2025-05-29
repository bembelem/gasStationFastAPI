from pydantic import BaseModel
from typing import Optional


class StationBase(BaseModel):
    name: str
    address: str
    contact_number: str


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    contact_number: Optional[str]


class StationResponse(StationBase):
    id: int

    class Config:
        from_attributes = True
