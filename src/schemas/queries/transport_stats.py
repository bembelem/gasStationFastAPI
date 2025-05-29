from pydantic import BaseModel
from typing import Optional

class TransportStats(BaseModel):
    transport_number: str
    transport_type: str
    status: str
    transfer_count: int
    total_volume_transferred: Optional[float]
    capacity: float
    avg_delivery_time_hours: Optional[float]
    incomplete_transfers: int
    current_location: Optional[str]

    class Config:
        orm_mode = True
