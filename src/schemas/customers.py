from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CustomerBase(BaseModel):
    phone_number: str = Field(..., description="Номер телефона клиента")
    registration_date: date = Field(..., description="Дата регистрации")
    bonus_points: int = Field(default=0, description="Бонусные баллы")
    client_tier_id: Optional[int] = Field(None, description="ID уровня клиента")
    total_purchases: float = Field(default=0, description="Сумма покупок")
    last_visit_date: Optional[date] = Field(None, description="Дата последнего визита")


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    phone_number: Optional[str]
    bonus_points: Optional[int]
    client_tier_id: Optional[int]
    total_purchases: Optional[float]
    last_visit_date: Optional[date]


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True
