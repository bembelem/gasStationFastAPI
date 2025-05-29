from pydantic import BaseModel
from typing import Optional

class RawMaterialEfficiencyAnalysis(BaseModel):
    raw_material_name: str
    raw_material_type: str
    supplier_name: str
    total_volume_used: float
    batch_count: int
    avg_volume_per_batch: float
    total_cost: float
    avg_efficiency_ratio: Optional[float]
    cost_per_output_unit: Optional[float]

    class Config:
        orm_mode = True