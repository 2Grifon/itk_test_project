from decimal import Decimal

from sqlmodel import Field

from app.core.base_models import UUIDModelBase


class Wallet(UUIDModelBase, table=True):
    """Модель кошелька"""

    __tablename__ = "wallet"

    # Модели пользователей у нас в ТЗ нет, так что привязки к ним тоже нет
    balance: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=18,
        ge=0,  # баланс не может быть отрицательным
    )
