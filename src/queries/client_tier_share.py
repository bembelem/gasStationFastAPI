from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.models import SaleTransaction, Customer, ClientTier

def get_client_tier_share_report(db: Session):
    # общая сумма успешных продаж (одна строка с total_purchase)
    total_purchase_subquery = (
        db.query(func.sum(SaleTransaction.total_amount).label("total_purchase"))
        .filter(SaleTransaction.status_id == 3)
        .scalar_subquery()
    )

    query = (
        db.query(
            ClientTier.name.label("client_tier"),
            func.sum(SaleTransaction.total_amount).label("tier_total_amount"),
            total_purchase_subquery.label("total_purchase"),
            (func.sum(SaleTransaction.total_amount) / total_purchase_subquery * 100).label("tier_purchase_percentage")
        )
        .join(Customer, SaleTransaction.customer_id == Customer.id, isouter=True)
        .join(ClientTier, Customer.client_tier_id == ClientTier.id, isouter=True)
        .filter(SaleTransaction.status_id == 3)
        .group_by(ClientTier.name)
        .order_by(func.sum(SaleTransaction.total_amount).desc())
    )

    return query.all()
