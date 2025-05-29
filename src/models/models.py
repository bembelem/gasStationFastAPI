from sqlalchemy import Column, Integer, Text, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class FuelType(Base):
    __tablename__ = "fuel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    refinery_tanks = relationship("RefineryTank", back_populates="fuel_type")
    station_tanks = relationship("StationTank", back_populates="fuel_type")
    fuel_pumps = relationship("FuelPump", back_populates="fuel_type")
    refueling_sessions = relationship("RefuelingSession", back_populates="fuel_type")
    supply_orders = relationship("SupplyOrder", back_populates="fuel_type")
    production_orders = relationship("ProductionOrder", back_populates="fuel_type")
    terminal_tanks = relationship("TerminalTank", back_populates="fuel_type")


class Refinery(Base):
    __tablename__ = "refineries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    address_line = Column(Text, nullable=False)

    refinery_tanks = relationship("RefineryTank", back_populates="refinery")
    storage_locations = relationship("StorageLocation", back_populates="refinery")
    production_units = relationship("ProductionUnit", back_populates="refinery")
    raw_materials_supply = relationship("RawMaterialsSupply", back_populates="refinery")
    production_orders = relationship("ProductionOrder", back_populates="refinery")


class RefineryTank(Base):
    __tablename__ = "refinery_tanks"

    id = Column(Integer, primary_key=True, index=True)
    refinery_id = Column(Integer, ForeignKey("refineries.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    capacity = Column(Float, nullable=False)
    current_volume = Column(Float, nullable=False)

    refinery = relationship("Refinery", back_populates="refinery_tanks")
    fuel_type = relationship("FuelType", back_populates="refinery_tanks")
    production_batches = relationship("ProductionBatchTankRefinery", back_populates="refinery_tank")


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    contact_number = Column(Text, nullable=False)

    station_tanks = relationship("StationTank", back_populates="station")
    fuel_dispensers = relationship("FuelDispenser", back_populates="station")
    supply_orders = relationship("SupplyOrder", back_populates="station")


class StationTank(Base):
    __tablename__ = "station_tanks"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    capacity = Column(Float, nullable=False)
    current_volume = Column(Float, nullable=False)

    station = relationship("Station", back_populates="station_tanks")
    fuel_type = relationship("FuelType", back_populates="station_tanks")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    details = Column(Text)

    payment_methods = relationship("PaymentMethod", back_populates="provider")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    type = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False)
    requires_authorization = Column(Boolean, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"))

    provider = relationship("Provider", back_populates="payment_methods")
    sale_transactions = relationship("SaleTransaction", back_populates="payment_method")


class SaleTransactionStatus(Base):
    __tablename__ = "sale_transaction_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    sale_transactions = relationship("SaleTransaction", back_populates="status")
    old_status_audits = relationship("SaleTransactionAudit", foreign_keys="SaleTransactionAudit.old_status_id",
                                     back_populates="old_status")
    new_status_audits = relationship("SaleTransactionAudit", foreign_keys="SaleTransactionAudit.new_status_id",
                                     back_populates="new_status")


class ClientTier(Base):
    __tablename__ = "client_tiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    customers = relationship("Customer", back_populates="client_tier")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Text, nullable=False, unique=True)
    registration_date = Column(Date, nullable=False)
    bonus_points = Column(Integer, nullable=False, default=0)
    client_tier_id = Column(Integer, ForeignKey("client_tiers.id"))
    total_purchases = Column(Float, nullable=False, default=0)
    last_visit_date = Column(Date)

    client_tier = relationship("ClientTier", back_populates="customers")
    sale_transactions = relationship("SaleTransaction", back_populates="customer")


class OperatorStatus(Base):
    __tablename__ = "operator_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    operators = relationship("Operator", back_populates="status")


class OperatorRole(Base):
    __tablename__ = "operator_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    operators = relationship("Operator", back_populates="role")


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    phone_number = Column(Text)
    email = Column(Text)
    status_id = Column(Integer, ForeignKey("operator_statuses.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("operator_roles.id"), nullable=False)
    password_hash = Column(Text, nullable=False)

    status = relationship("OperatorStatus", back_populates="operators")
    role = relationship("OperatorRole", back_populates="operators")
    sale_transactions = relationship("SaleTransaction", back_populates="operator")


class SaleTransaction(Base):
    __tablename__ = "sale_transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    transaction_date_time = Column(DateTime, nullable=False)
    bonus_used = Column(Integer, default=0)
    volume = Column(Float, nullable=False)
    currency = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey("sale_transaction_statuses.id"), nullable=False)

    customer = relationship("Customer", back_populates="sale_transactions")
    operator = relationship("Operator", back_populates="sale_transactions")
    payment_method = relationship("PaymentMethod", back_populates="sale_transactions")
    status = relationship("SaleTransactionStatus", back_populates="sale_transactions")
    audits = relationship("SaleTransactionAudit", back_populates="sale_transaction")
    refueling_sessions = relationship("RefuelingSession", back_populates="sale_transaction")


class SaleTransactionAudit(Base):
    __tablename__ = "sale_transaction_audit"

    id = Column(Integer, primary_key=True, index=True)
    sale_transaction_id = Column(Integer, ForeignKey("sale_transactions.id"), nullable=False)
    changed_at = Column(DateTime, nullable=False)
    old_status_id = Column(Integer, ForeignKey("sale_transaction_statuses.id"))
    new_status_id = Column(Integer, ForeignKey("sale_transaction_statuses.id"), nullable=False)
    comments = Column(Text)

    sale_transaction = relationship("SaleTransaction", back_populates="audits")
    old_status = relationship("SaleTransactionStatus", foreign_keys=[old_status_id], back_populates="old_status_audits")
    new_status = relationship("SaleTransactionStatus", foreign_keys=[new_status_id], back_populates="new_status_audits")


class RefuelingSessionStatus(Base):
    __tablename__ = "refueling_session_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    refueling_sessions = relationship("RefuelingSession", back_populates="status")


class FuelDispenser(Base):
    __tablename__ = "fuel_dispensers"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    is_active = Column(Boolean, nullable=False)

    station = relationship("Station", back_populates="fuel_dispensers")
    fuel_pumps = relationship("FuelPump", back_populates="fuel_dispenser")


class FuelPump(Base):
    __tablename__ = "fuel_pumps"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    fuel_dispenser_id = Column(Integer, ForeignKey("fuel_dispensers.id"), nullable=False)
    nozzle_number = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)

    fuel_type = relationship("FuelType", back_populates="fuel_pumps")
    fuel_dispenser = relationship("FuelDispenser", back_populates="fuel_pumps")
    refueling_sessions = relationship("RefuelingSession", back_populates="fuel_pump")


class RefuelingSession(Base):
    __tablename__ = "refueling_sessions"

    id = Column(Integer, primary_key=True, index=True)
    fuel_pump_id = Column(Integer, ForeignKey("fuel_pumps.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    volume = Column(Float, nullable=False)
    authorized_volume = Column(Float)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime)
    status_id = Column(Integer, ForeignKey("refueling_session_statuses.id"), nullable=False)
    sale_transaction_id = Column(Integer, ForeignKey("sale_transactions.id"), nullable=False)

    fuel_pump = relationship("FuelPump", back_populates="refueling_sessions")
    fuel_type = relationship("FuelType", back_populates="refueling_sessions")
    status = relationship("RefuelingSessionStatus", back_populates="refueling_sessions")
    sale_transaction = relationship("SaleTransaction", back_populates="refueling_sessions")


class StorageLocation(Base):
    __tablename__ = "storage_locations"

    id = Column(Integer, primary_key=True, index=True)
    refinery_id = Column(Integer, ForeignKey("refineries.id"), nullable=False)
    name = Column(Text, nullable=False)

    refinery = relationship("Refinery", back_populates="storage_locations")
    delivery_items = relationship("DeliveryItem", back_populates="storage_location")


class ProductionUnitStatus(Base):
    __tablename__ = "production_unit_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    production_units = relationship("ProductionUnit", back_populates="status")


class ProductionUnit(Base):
    __tablename__ = "production_units"

    id = Column(Integer, primary_key=True, index=True)
    refinery_id = Column(Integer, ForeignKey("refineries.id"), nullable=False)
    name = Column(Text, nullable=False)
    capacity_per_day = Column(Float, nullable=False)
    last_maintenance = Column(Date)
    status_id = Column(Integer, ForeignKey("production_unit_statuses.id"), nullable=False)

    refinery = relationship("Refinery", back_populates="production_units")
    status = relationship("ProductionUnitStatus", back_populates="production_units")
    production_batches = relationship("ProductionBatchUnit", back_populates="production_unit")


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    raw_materials_supply = relationship("RawMaterialsSupply", back_populates="status")
    supply_orders = relationship("SupplyOrder", back_populates="status")
    production_orders = relationship("ProductionOrder", back_populates="status")


class BatchStatus(Base):
    __tablename__ = "batch_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    production_batches = relationship("ProductionBatch", back_populates="status")


class ProductionBatch(Base):
    __tablename__ = "production_batches"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    expected_output_volume = Column(Float, nullable=False)
    status_id = Column(Integer, ForeignKey("batch_statuses.id"), nullable=False)

    status = relationship("BatchStatus", back_populates="production_batches")
    refinery_tanks = relationship("ProductionBatchTankRefinery", back_populates="production_batch")
    raw_materials = relationship("ProductionBatchRawMaterial", back_populates="production_batch")
    production_units = relationship("ProductionBatchUnit", back_populates="production_batch")


class ProductionBatchTankRefinery(Base):
    __tablename__ = "production_batch_tank_refineries"

    production_batch_id = Column(Integer, ForeignKey("production_batches.id"), primary_key=True)
    refinary_tank_id = Column(Integer, ForeignKey("refinery_tanks.id"), primary_key=True)

    production_batch = relationship("ProductionBatch", back_populates="refinery_tanks")
    refinery_tank = relationship("RefineryTank", back_populates="production_batches")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)

    raw_materials_supply = relationship("RawMaterialsSupply", back_populates="supplier")


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    quality_parameter = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(Text, nullable=False)

    raw_materials_supply = relationship("RawMaterialsSupply", back_populates="raw_material")
    delivery_items = relationship("DeliveryItem", back_populates="raw_material")


class RawMaterialsSupply(Base):
    __tablename__ = "raw_materials_supply"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False)
    refinery_id = Column(Integer, ForeignKey("refineries.id"), nullable=False)
    delivery_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    quality_check_passed = Column(Boolean)
    status_id = Column(Integer, ForeignKey("order_statuses.id"), nullable=False)

    supplier = relationship("Supplier", back_populates="raw_materials_supply")
    raw_material = relationship("RawMaterial", back_populates="raw_materials_supply")
    refinery = relationship("Refinery", back_populates="raw_materials_supply")
    status = relationship("OrderStatus", back_populates="raw_materials_supply")
    deliveries = relationship("RawMaterialsDelivery", back_populates="supply")


class RawMaterialsDelivery(Base):
    __tablename__ = "raw_materials_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(Integer, ForeignKey("raw_materials_supply.id"), nullable=False)
    received_at = Column(DateTime, nullable=False)

    supply = relationship("RawMaterialsSupply", back_populates="deliveries")
    delivery_items = relationship("DeliveryItem", back_populates="delivery")


class DeliveryItem(Base):
    __tablename__ = "delivery_items"

    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("raw_materials_deliveries.id"), nullable=False)
    storage_location_id = Column(Integer, ForeignKey("storage_locations.id"), nullable=False)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False)
    deliveried_at = Column(DateTime, nullable=False)

    delivery = relationship("RawMaterialsDelivery", back_populates="delivery_items")
    storage_location = relationship("StorageLocation", back_populates="delivery_items")
    raw_material = relationship("RawMaterial", back_populates="delivery_items")
    production_batches = relationship("ProductionBatchRawMaterial", back_populates="delivery_item")


class ProductionBatchRawMaterial(Base):
    __tablename__ = "production_batch_raw_materials"

    production_batch_id = Column(Integer, ForeignKey("production_batches.id"), primary_key=True)
    delivery_item_id = Column(Integer, ForeignKey("delivery_items.id"), primary_key=True)
    volume = Column(Float, nullable=False)

    production_batch = relationship("ProductionBatch", back_populates="raw_materials")
    delivery_item = relationship("DeliveryItem", back_populates="production_batches")


class ProductionBatchUnit(Base):
    __tablename__ = "production_batch_units"

    production_batch_id = Column(Integer, ForeignKey("production_batches.id"), primary_key=True)
    production_unit_id = Column(Integer, ForeignKey("production_units.id"), primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)

    production_batch = relationship("ProductionBatch", back_populates="production_units")
    production_unit = relationship("ProductionUnit", back_populates="production_batches")


class TankType(Base):
    __tablename__ = "tank_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    source_transfers = relationship("FuelTransfer", foreign_keys="FuelTransfer.source_type_id",
                                    back_populates="source_type")
    destination_transfers = relationship("FuelTransfer", foreign_keys="FuelTransfer.destination_type_id",
                                         back_populates="destination_type")


class TransferStatus(Base):
    __tablename__ = "transfer_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    fuel_transfers = relationship("FuelTransfer", back_populates="status")


class OrderType(Base):
    __tablename__ = "order_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    fuel_transfers = relationship("FuelTransfer", back_populates="order_type")


class TransportStatus(Base):
    __tablename__ = "transport_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    transports = relationship("Transport", back_populates="status_ref")


class Transport(Base):
    __tablename__ = "transports"

    id = Column(Integer, primary_key=True, index=True)
    transport_number = Column(Text, nullable=False)
    transport_type = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)
    status = Column(Integer, ForeignKey("transport_statuses.id"), nullable=False)
    current_location = Column(Text)

    status_ref = relationship("TransportStatus", back_populates="transports")
    transfers = relationship("TransferTransport", back_populates="transport")


class Terminal(Base):
    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    address_line = Column(Text, nullable=False)

    terminal_tanks = relationship("TerminalTank", back_populates="terminal")
    production_orders = relationship("ProductionOrder", back_populates="terminal")


class TerminalTank(Base):
    __tablename__ = "terminal_tanks"

    id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(Integer, ForeignKey("terminals.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    capacity = Column(Float, nullable=False)
    current_volume = Column(Float, nullable=False)

    terminal = relationship("Terminal", back_populates="terminal_tanks")
    fuel_type = relationship("FuelType", back_populates="terminal_tanks")


class SupplyOrder(Base):
    __tablename__ = "supply_orders"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    supply_date = Column(Date, nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("order_statuses.id"), nullable=False)

    fuel_type = relationship("FuelType", back_populates="supply_orders")
    station = relationship("Station", back_populates="supply_orders")
    status = relationship("OrderStatus", back_populates="supply_orders")


class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(Integer, ForeignKey("terminals.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    refinery_id = Column(Integer, ForeignKey("refineries.id"), nullable=False)
    volume_requested = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    required_by_date = Column(Date, nullable=False)
    priority = Column(Integer, nullable=False)
    status_id = Column(Integer, ForeignKey("order_statuses.id"), nullable=False)

    terminal = relationship("Terminal", back_populates="production_orders")
    fuel_type = relationship("FuelType", back_populates="production_orders")
    refinery = relationship("Refinery", back_populates="production_orders")
    status = relationship("OrderStatus", back_populates="production_orders")


class FuelTransfer(Base):
    __tablename__ = "fuel_transfers"

    id = Column(Integer, primary_key=True, index=True)
    source_type_id = Column(Integer, ForeignKey("tank_types.id"), nullable=False)
    source_id = Column(Integer, nullable=False)
    destination_type_id = Column(Integer, ForeignKey("tank_types.id"), nullable=False)
    destination_id = Column(Integer, nullable=False)
    order_type_id = Column(Integer, ForeignKey("order_types.id"), nullable=False)
    order_id = Column(Integer, nullable=False)
    volume = Column(Float, nullable=False)
    dispatched_at = Column(DateTime, nullable=False)
    received_at = Column(DateTime)
    status_id = Column(Integer, ForeignKey("transfer_statuses.id"), nullable=False)

    source_type = relationship("TankType", foreign_keys=[source_type_id], back_populates="source_transfers")
    destination_type = relationship("TankType", foreign_keys=[destination_type_id],
                                    back_populates="destination_transfers")
    status = relationship("TransferStatus", back_populates="fuel_transfers")
    order_type = relationship("OrderType", back_populates="fuel_transfers")
    transports = relationship("TransferTransport", back_populates="transfer")


class TransferTransport(Base):
    __tablename__ = "transfer_transports"

    transfer_id = Column(Integer, ForeignKey("fuel_transfers.id"), primary_key=True)
    transport_id = Column(Integer, ForeignKey("transports.id"), primary_key=True)
    volume = Column(Float, nullable=False)

    transfer = relationship("FuelTransfer", back_populates="transports")
    transport = relationship("Transport", back_populates="transfers")