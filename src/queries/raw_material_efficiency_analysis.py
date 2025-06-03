from sqlalchemy.orm import Session
from sqlalchemy import func, text, case
from src.models.models import (
    RawMaterial, DeliveryItem, RawMaterialsDelivery, RawMaterialsSupply,
    Supplier, ProductionBatchRawMaterial, ProductionBatch, BatchStatus
)


def get_raw_material_efficiency_analysis(db: Session):
    # CTE 1: Raw Material Consumption
    raw_material_consumption = (
        db.query(
            RawMaterial.id.label("raw_material_id"),
            RawMaterial.name.label("raw_material_name"),
            RawMaterial.type.label("raw_material_type"),
            Supplier.id.label("supplier_id"),
            Supplier.name.label("supplier_name"),
            func.sum(ProductionBatchRawMaterial.volume).label("total_volume_used"),
            func.count(ProductionBatch.id.distinct()).label("batch_count"),
            func.avg(ProductionBatchRawMaterial.volume).label("avg_volume_per_batch"),
            func.sum(ProductionBatchRawMaterial.volume * RawMaterial.price_per_unit).label("total_cost")
        )
        .join(DeliveryItem, DeliveryItem.raw_material_id == RawMaterial.id)
        .join(RawMaterialsDelivery, RawMaterialsDelivery.id == DeliveryItem.delivery_id)
        .join(RawMaterialsSupply, RawMaterialsSupply.id == RawMaterialsDelivery.supply_id)
        .join(Supplier, Supplier.id == RawMaterialsSupply.supplier_id)
        .join(ProductionBatchRawMaterial, ProductionBatchRawMaterial.delivery_item_id == DeliveryItem.id)
        .join(ProductionBatch, ProductionBatch.id == ProductionBatchRawMaterial.production_batch_id)
        .filter(ProductionBatch.start_time >= text("DATE('now', '-3 months')"))
        .group_by(RawMaterial.id, Supplier.id)
        .subquery()
    )

    # CTE 2: Batch Efficiency
    batch_efficiency = (
        db.query(
            ProductionBatch.id.label("batch_id"),
            func.sum(ProductionBatchRawMaterial.volume).label("total_raw_materials"),
            ProductionBatch.expected_output_volume.label("expected_output_volume"),
            (ProductionBatch.expected_output_volume /
             func.nullif(func.sum(ProductionBatchRawMaterial.volume), 0)).label("efficiency_ratio"),
            BatchStatus.name.label("batch_status")
        )
        .join(BatchStatus, BatchStatus.id == ProductionBatch.status_id)
        .join(ProductionBatchRawMaterial, ProductionBatchRawMaterial.production_batch_id == ProductionBatch.id)
        .group_by(ProductionBatch.id)
        .subquery()
    )

    query = (
        db.query(
            raw_material_consumption.c.raw_material_name,
            raw_material_consumption.c.raw_material_type,
            raw_material_consumption.c.supplier_name,
            raw_material_consumption.c.total_volume_used,
            raw_material_consumption.c.batch_count,
            raw_material_consumption.c.avg_volume_per_batch,
            raw_material_consumption.c.total_cost,
            func.avg(batch_efficiency.c.efficiency_ratio).label("avg_efficiency_ratio"),
            (raw_material_consumption.c.total_cost /
             func.nullif(func.sum(batch_efficiency.c.expected_output_volume), 0)).label("cost_per_output_unit")
        )
        .join(DeliveryItem, DeliveryItem.raw_material_id == raw_material_consumption.c.raw_material_id)
        .join(RawMaterialsDelivery, RawMaterialsDelivery.id == DeliveryItem.delivery_id)
        .join(RawMaterialsSupply, RawMaterialsSupply.id == RawMaterialsDelivery.supply_id)
        .join(ProductionBatchRawMaterial, ProductionBatchRawMaterial.delivery_item_id == DeliveryItem.id)
        .filter(RawMaterialsSupply.supplier_id == raw_material_consumption.c.supplier_id)

        .join(batch_efficiency, batch_efficiency.c.batch_id == ProductionBatchRawMaterial.production_batch_id)
        .group_by(
            raw_material_consumption.c.raw_material_id,
            raw_material_consumption.c.supplier_id
        )
        .order_by(text("cost_per_output_unit ASC"))
    )

    return query.all()
