from pydantic import BaseModel

class FuelLevelResponse(BaseModel):
    station: str
    address: str
    fuel_type: str
    current_volume: float
    capacity: float
    fill_percentage: float
    stock_status: str
