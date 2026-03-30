from uuid import UUID

from fastapi import APIRouter

from app.modules.wallet.schemas import WalletOperationRequest, WalletResponse

from app.modules.wallet.services import WalletServiceDependency

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(wallet_id: UUID, service: WalletServiceDependency) -> WalletResponse:
    """Получить текущий баланс кошелька."""
    wallet = await service.get_wallet(wallet_id)
    return WalletResponse(id=wallet.id, balance=wallet.balance)


@router.post("/{wallet_id}/operation", response_model=WalletResponse)
async def wallet_operation(
    wallet_id: UUID,
    body: WalletOperationRequest,
    service: WalletServiceDependency,
) -> WalletResponse:
    """Изменить баланс кошелька"""
    wallet = await service.perform_operation(wallet_id, body)
    return WalletResponse(id=wallet.id, balance=wallet.balance)
