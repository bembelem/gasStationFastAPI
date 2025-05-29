from pydantic import BaseModel, Field
from typing import Optional

class FuelPurchaseRequest(BaseModel):
    station_id: int = Field(..., description="ID станции")
    fuel_type_id: int = Field(..., description="ID типа топлива")
    fuel_pump_id: int = Field(..., description="ID топливной колонки")
    volume: float = Field(..., gt=0, description="Объем топлива в литрах")
    total_amount: float = Field(..., gt=0, description="Общая сумма к оплате")
    customer_id: Optional[int] = Field(None, description="ID клиента (опционально)")
    operator_id: Optional[int] = Field(None, description="ID оператора")
    payment_method_id: Optional[int] = Field(None, description="ID способа оплаты")
    bonus_used: float = Field(0.0, ge=0, description="Использованные бонусы")

class FuelPurchaseResponse(BaseModel):
    success: bool
    sale_transaction_id: int
    refueling_session_id: int
    bonus_points_added: int
    volume_dispensed: float
    total_amount: float