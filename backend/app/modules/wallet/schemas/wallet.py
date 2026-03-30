from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

Amount = Annotated[Decimal, Field(ge=0, decimal_places=2, max_digits=18)]


class OperationType(StrEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationRequest(BaseModel):
    """Изменение баланса кошелька"""

    operation_type: OperationType
    amount: Amount


class WalletResponse(BaseModel):
    """Получение баланса кошелька"""

    id: UUID
    balance: Amount
