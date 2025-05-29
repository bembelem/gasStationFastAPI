from pydantic import BaseModel, Field
from typing import Optional

class RefineryBase(BaseModel):
    name: str = Field(..., description="Название НПЗ")
    address_line: str = Field(..., description="Адрес")

class RefineryCreate(RefineryBase):
    pass

class RefineryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название НПЗ")
    address_line: Optional[str] = Field(None, description="Адрес")

class RefineryResponse(RefineryBase):
    id: int

    class Config:
        from_attributes = True
