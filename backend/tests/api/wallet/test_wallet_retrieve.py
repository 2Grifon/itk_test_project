import uuid
from decimal import Decimal

from fastapi import HTTPException, status


def test_get_wallet_ok(client, fake_service):
    wallet = fake_service.wallet

    response = client.get(f"/wallets/{wallet.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(wallet.id)
    assert Decimal(response.json()["balance"]) == wallet.balance


def test_get_wallet_not_found(client, fake_service):
    def raise_404(wallet_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    fake_service.get_wallet = raise_404

    response = client.get(f"/wallets/{uuid.uuid4()}")

    assert response.status_code == 404
