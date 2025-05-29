from pydantic import BaseModel

class FuelSalesRank(BaseModel):
    station_name: str
    fuel_name: str
    sales: float
    fuel_sales_rank: int

    class Config:
        orm_mode = True
