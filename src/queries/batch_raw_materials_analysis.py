from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from src.models.models import (
    RawMaterial, DeliveryItem, ProductionBatchRawMaterial,
    ProductionBatch, RawMaterialsDelivery, RawMaterialsSupply
)


def get_batch_raw_materials_analysis(db: Session):
    # Подзапрос для среднего значения Expected_Output_Volume
    avg_subquery = (
        db.query(func.avg(ProductionBatch.expected_output_volume))
        .scalar_subquery()
    )

    query = (
        db.query(
            RawMaterial.name.label("name"),
            ProductionBatch.expected_output_volume.label("expected_output_volume"),
            RawMaterialsSupply.quality_check_passed.label("quality_check_passed"),
            cast(
                cast(RawMaterialsSupply.supplier_id, String) + ' -> ' +
                cast(RawMaterialsDelivery.supply_id, String) + ' -> ' +
                cast(DeliveryItem.delivery_id, String) + ' -> ' +
                cast(RawMaterialsSupply.refinery_id, String),
                String
            ).label("way")
        )
        .select_from(RawMaterial)
        .join(RawMaterial.delivery_items)
        .join(ProductionBatchRawMaterial, DeliveryItem.id == ProductionBatchRawMaterial.delivery_item_id)
        .join(ProductionBatch, ProductionBatchRawMaterial.production_batch_id == ProductionBatch.id)
        .join(RawMaterialsDelivery, DeliveryItem.delivery_id == RawMaterialsDelivery.id)
        .join(RawMaterialsSupply, RawMaterialsDelivery.supply_id == RawMaterialsSupply.id)
        .filter(
            ProductionBatch.status_id == 3,
            ProductionBatch.expected_output_volume < avg_subquery
        )
        .order_by(RawMaterial.name, DeliveryItem.delivery_id)
    )

    return query.all()
