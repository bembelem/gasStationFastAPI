from fastapi import FastAPI

from .fuel_types import router as fuel_types_router
from .refinery_tanks import router as refinery_tanks_router
from .refineries import router as refineries_router
from .stations import router as stations_router
from .station_tanks import router as stations_tanks_router
from .customers import router as customers_router

from .queries.fuel_level_status import router as fuel_level_router
from .queries.fuel_deficit_report import router as fuel_deficit_router
from .queries.hourly_sales_report import router as sales_by_hour_router
from .queries.client_tier_share import router as client_tier_share_router
from .queries.transport_stats import router as transport_stats_router
from .queries.fuel_sales_rank import router as fuel_sales_rank_router
from .queries.batch_raw_materials_analysis import router as raw_material_analysis_router
from .queries.raw_material_efficiency_analysis import router as raw_material_efficiency_analysis_router
from .queries.fuel_supply_chain_analysis import router as fuel_supply_chain_analysis_router
from .fuel_purchase import router as fuel_purchase_router

# Все ручки
ALL_ROUTERS = [
    fuel_types_router,
    refineries_router,
    refinery_tanks_router,
    stations_tanks_router,
    stations_router,
    customers_router,
    fuel_level_router,
    fuel_deficit_router,
    sales_by_hour_router,
    client_tier_share_router,
    transport_stats_router,
    fuel_sales_rank_router,
    raw_material_analysis_router,
    raw_material_efficiency_analysis_router,
    fuel_supply_chain_analysis_router,
    fuel_purchase_router
]


def setup_routers(app: FastAPI):

    for router in ALL_ROUTERS:
        app.include_router(router)


__all__ = ["setup_routers", "ALL_ROUTERS"]