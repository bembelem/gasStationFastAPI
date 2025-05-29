from pydantic import BaseModel

class HourlySalesResponse(BaseModel):
    station: str
    fuel_type: str
    hour_of_day: str
    transaction_count: int
    total_volume: float
    total_amount: float
    average_receipt: float
    average_volume_per_transaction: float