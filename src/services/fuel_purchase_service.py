from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, text
from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException

from src.models.models import (
    StationTank, SaleTransaction, RefuelingSession, Customer,
    SaleTransactionStatus, RefuelingSessionStatus
)


class FuelPurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def process_fuel_purchase(
            self,
            station_id: int,
            fuel_type_id: int,
            fuel_pump_id: int,
            volume: float,
            total_amount: float,
            customer_id: Optional[int] = None,
            operator_id: Optional[int] = None,
            payment_method_id: Optional[int] = None,
            bonus_used: float = 0.0
    ) -> dict:

        try:
            # Начинаем транзакцию
            with self.db.begin():
                # 1. Проверяем и списываем топливо из бака
                tank_updated = self._deduct_fuel_from_tank(
                    station_id, fuel_type_id, volume
                )

                if not tank_updated:
                    raise HTTPException(
                        status_code=400,
                        detail="Недостаточно топлива в баке или бак не найден"
                    )

                # 2. Создаем транзакцию продажи
                sale_transaction = self._create_sale_transaction(
                    customer_id=customer_id,
                    operator_id=operator_id,
                    payment_method_id=payment_method_id,
                    total_amount=total_amount,
                    bonus_used=bonus_used,
                    volume=volume
                )

                # 3. Создаем сессию заправки
                refueling_session = self._create_refueling_session(
                    fuel_pump_id=fuel_pump_id,
                    fuel_type_id=fuel_type_id,
                    volume=volume,
                    sale_transaction_id=sale_transaction.id
                )

                # 4. Начисляем бонусы клиенту (если есть)
                bonus_points_added = 0
                if customer_id:
                    bonus_points_added = self._update_customer_bonuses(
                        customer_id, total_amount
                    )

                # Коммит происходит автоматически при выходе из with

                return {
                    "success": True,
                    "sale_transaction_id": sale_transaction.id,
                    "refueling_session_id": refueling_session.id,
                    "bonus_points_added": bonus_points_added,
                    "volume_dispensed": volume,
                    "total_amount": total_amount
                }

        except SQLAlchemyError as e:
            # Rollback автоматический при исключении
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка базы данных: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка: {str(e)}"
            )

    def _deduct_fuel_from_tank(
            self, station_id: int, fuel_type_id: int, volume: float
    ) -> bool:
        rows_affected = (
            self.db.query(StationTank)
            .filter(
                StationTank.station_id == station_id,
                StationTank.fuel_type_id == fuel_type_id,
                StationTank.current_volume >= volume
            )
            .update({
                StationTank.current_volume: StationTank.current_volume - volume
            })
        )
        return rows_affected > 0

    def _create_sale_transaction(
            self,
            customer_id: Optional[int],
            operator_id: Optional[int],
            payment_method_id: Optional[int],
            total_amount: float,
            bonus_used: float,
            volume: float
    ) -> SaleTransaction:
        # Получаем ID статуса 'completed'
        completed_status = (
            self.db.query(SaleTransactionStatus.id)
            .filter(SaleTransactionStatus.name == 'Completed')
            .scalar()
        )


        sale_transaction = SaleTransaction(
            customer_id=customer_id,
            operator_id=operator_id,
            payment_method_id=payment_method_id,
            total_amount=total_amount,
            transaction_date_time=datetime.now(),
            bonus_used=bonus_used,
            volume=volume,
            currency='RUB',
            status_id=completed_status
        )

        self.db.add(sale_transaction)
        self.db.flush()  # Получаем ID без коммита
        return sale_transaction

    def _create_refueling_session(
            self,
            fuel_pump_id: int,
            fuel_type_id: int,
            volume: float,
            sale_transaction_id: int
    ) -> RefuelingSession:
        # Получаем ID статуса 'finished'
        finished_status = (
            self.db.query(RefuelingSessionStatus.id)
            .filter(RefuelingSessionStatus.name == 'Completed')
            .scalar()
        )

        current_time = datetime.now()

        refueling_session = RefuelingSession(
            fuel_pump_id=fuel_pump_id,
            fuel_type_id=fuel_type_id,
            volume=volume,
            authorized_volume=volume,
            started_at=current_time,
            finished_at=current_time,
            status_id=finished_status,
            sale_transaction_id=sale_transaction_id
        )

        self.db.add(refueling_session)
        self.db.flush()
        return refueling_session

    def _update_customer_bonuses(
            self, customer_id: int, total_amount: float
    ) -> int:
        bonus_points = int(total_amount * 0.01)

        rows_affected = (
            self.db.query(Customer)
            .filter(Customer.id == customer_id)
            .update({
                Customer.bonus_points: Customer.bonus_points + bonus_points,
                Customer.total_purchases: Customer.total_purchases + total_amount,
                Customer.last_visit_date: date.today()
            })
        )

        return bonus_points if rows_affected > 0 else 0
