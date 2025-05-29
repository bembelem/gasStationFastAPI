from pydantic import BaseModel
from typing import Optional

class ClientTierShareReport(BaseModel):
    client_tier: Optional[str]
    tier_total_amount: float
    total_purchase: float
    tier_purchase_percentage: float

    class Config:
        orm_mode = True
