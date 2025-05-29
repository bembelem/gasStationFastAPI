from pydantic import BaseModel

class FuelSupplyChainAnalysis(BaseModel):
    id: int
    name: str
    address: str
    contact_number: str
    way: str

    class Config:
        orm_mode = True
