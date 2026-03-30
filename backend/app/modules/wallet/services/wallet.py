from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel import select

from app.core.db import SessionDependency
from app.modules.wallet.models import Wallet
from app.modules.wallet.schemas import OperationType, WalletOperationRequest


class WalletService:
    def __init__(self, session: SessionDependency) -> None:
        self.session = session

    async def get_wallet(self, wallet_id: UUID) -> Wallet:
        """Получить кошелёк по ID"""
        wallet: Wallet = await self.session.get(Wallet, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet {wallet_id} not found",
            )
        return wallet

    async def get_wallet_for_update(self, wallet_id: UUID) -> Wallet:
        """
        Получить кошелёк с блокировкой строки (FOR UPDATE), чтоб избежать проблемы
        с параллельными транзакциями
        """
        statement = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        result = await self.session.exec(statement)
        wallet: Wallet = result.one_or_none()

        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet {wallet_id} not found",
            )
        return wallet

    async def perform_operation(
        self,
        wallet_id: UUID,
        operation: WalletOperationRequest,
    ) -> Wallet:
        """
        Выполнить операцию DEPOSIT или WITHDRAW.
        """
        wallet: Wallet = await self.get_wallet_for_update(wallet_id)

        if operation.operation_type == OperationType.DEPOSIT:
            wallet.balance += operation.amount

        elif operation.operation_type == OperationType.WITHDRAW:

            if wallet.balance < operation.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient funds: "
                        f"balance={wallet.balance}, "
                        f"requested={operation.amount}"
                    ),
                )
            wallet.balance -= operation.amount

        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)

        return wallet


WalletServiceDependency = Annotated[WalletService, Depends(WalletService)]
